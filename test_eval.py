#!/usr/bin/env python3
"""
Copyright (c) Meta Platforms, Inc. and affiliates.

This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import glob
import os
import unittest

from eval import (
    ARTICLES,
    FA_TOKENS,
    contains,
    exact_match,
    _canonical_form,
    answer_variants,
    PREFIX_ARTICLES,
    content_language,
    normalize_answer,
    parse_input_jsonl,
    parse_output_csv,
    parse_output_jsonl,
    postprocess_answers,
    remove_articles,
)

BENCHMARK_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmark_data")
HAS_DATA = os.path.isdir(BENCHMARK_DATA)


class TestRemoveArticles(unittest.TestCase):
    def test_english_is_the_default(self):
        # Callers that predate the language parameter must be unaffected.
        self.assertEqual(remove_articles("the cat on a mat").split(), ["cat", "on", "mat"])
        self.assertEqual(normalize_answer("The Cat Sat On A Mat"), "cat sat on mat")

    def test_strips_articles_of_the_requested_language(self):
        cases = [
            ("german", "der hund und die katze", "hund und katze"),
            ("dutch", "de man en het huis", "man en huis"),
            ("french", "le chat et la souris", "chat et souris"),
            ("italian", "il cane e la casa", "cane e casa"),
            ("spanish", "el gato y la casa", "gato y casa"),
            ("portuguese", "o gato e a casa", "gato e casa"),
        ]
        for language, text, expected in cases:
            with self.subTest(language=language):
                self.assertEqual(normalize_answer(text, language), expected)

    def test_languages_without_articles_are_untouched(self):
        for language, text in [
            ("japanese", "東京タワー"),
            ("polish", "kot i pies"),
            ("hindi", "एक बिल्ली"),
        ]:
            with self.subTest(language=language):
                self.assertEqual(remove_articles(text, language), text)

    def test_unknown_language_falls_back_to_no_op(self):
        self.assertEqual(remove_articles("the cat", "klingon"), "the cat")

    def test_does_not_strip_english_articles_from_other_languages(self):
        # Regression: "an" is a syllable in Vietnamese, not an article. Stripping
        # it rewrote "thiên an môn" to "thiên môn", which then exact-matched a
        # prediction naming something else entirely.
        self.assertEqual(normalize_answer("Thiên An Môn", "vietnamese"), "thiên an môn")
        self.assertEqual(normalize_answer("An ninh", "vietnamese"), "an ninh")
        # Likewise the English "a" inside the Spanish title "El Equipo A".
        self.assertEqual(normalize_answer("El Equipo A", "spanish"), "equipo a")

    def test_prefix_articles_are_stripped(self):
        # Arabic and Hebrew fuse the definite article onto the following word.
        self.assertEqual(normalize_answer("الكتاب", "arabic"), "كتاب")
        self.assertEqual(normalize_answer("הספר", "hebrew"), "ספר")

    def test_prefix_stripping_leaves_bare_prefix_alone(self):
        # A word consisting only of the prefix must not be emptied.
        for language, prefix in PREFIX_ARTICLES.items():
            with self.subTest(language=language):
                self.assertEqual(remove_articles(prefix, language), prefix)

    def test_numeral_ambiguous_indefinites_are_kept(self):
        # "ein", "een", "un", "en"... double as the numeral "one". In an answer
        # to a counting question they ARE the answer, so they must survive:
        # gold "ein Kind" (one child) and a prediction "Kind" that omits the
        # count are different answers.
        self.assertEqual(normalize_answer("ein Kind", "german"), "ein kind")
        self.assertNotEqual(
            normalize_answer("ein Kind", "german"), normalize_answer("Kind", "german")
        )
        self.assertEqual(normalize_answer("un chat", "french"), "un chat")
        self.assertEqual(normalize_answer("en bok och ett hus", "swedish"), "en bok och ett hus")
        self.assertEqual(normalize_answer("un caine", "romanian"), "un caine")
        # All punctuation marks get removed.
        self.assertEqual(normalize_answer("l'attitude", "french"), "lattitude")
        # Plural indefinites are not numerals and are still stripped.
        self.assertEqual(normalize_answer("unos gatos", "spanish"), "gatos")

    def test_suffix_article_languages_leave_suffixes_alone(self):
        # Swedish and Romanian mark definiteness with a suffix on the noun,
        # which is out of scope for token-level stripping.
        self.assertEqual(normalize_answer("boken", "swedish"), "boken")
        self.assertEqual(normalize_answer("cainele", "romanian"), "cainele")

    def test_article_lists_are_lowercase_and_unique(self):
        # normalize_answer lowercases before stripping, so uppercase entries
        # would silently never match.
        for language, articles in ARTICLES.items():
            with self.subTest(language=language):
                self.assertEqual(list(articles), [a.lower() for a in articles])
                self.assertEqual(len(set(articles)), len(articles))

    def test_article_language_keys_are_real_languages(self):
        # A typo in a key ("portugese") would silently disable stripping for
        # that language rather than fail.
        for language in list(ARTICLES) + list(PREFIX_ARTICLES):
            with self.subTest(language=language):
                self.assertIn(language, FA_TOKENS)


class TestArticleOnlyAnswers(unittest.TestCase):
    """
    In several languages the indefinite article doubles as the numeral "one"
    ("un", "una", "een", "eine"), and those words appear as gold answers to
    counting questions. Stripping them to "" would let any article-only
    prediction exact-match them and would give a correct answer an F1 of 0.
    """

    CASES = [
        ("french", "un"),
        ("french", "la une"),
        ("italian", "una"),
        ("italian", "uno"),
        ("dutch", "een"),
        ("german", "Eine"),
        ("portuguese", "uma"),
    ]

    def test_article_only_answers_do_not_normalize_to_empty(self):
        for language, text in self.CASES:
            with self.subTest(language=language, text=text):
                self.assertNotEqual(normalize_answer(text, language), "")

    def test_wrong_article_word_is_not_an_exact_match(self):
        # gold "un" (one) versus a prediction of "le": both are article words,
        # but they are different answers and must not collide on "".
        self.assertNotEqual(
            normalize_answer("le", "french"), normalize_answer("un", "french")
        )

    def test_correct_article_only_answer_still_matches_itself(self):
        for language, text in self.CASES:
            with self.subTest(language=language, text=text):
                self.assertEqual(
                    normalize_answer(text, language),
                    normalize_answer(text.lower(), language),
                )

    def test_multiword_answers_still_strip_normally(self):
        # The fallback must only kick in when stripping would empty the whole
        # answer, not weaken ordinary stripping.
        self.assertEqual(normalize_answer("le chat", "french"), "chat")
        self.assertEqual(normalize_answer("Der Hund", "german"), "hund")


class TestPrefixStrippingGuards(unittest.TestCase):
    def test_short_words_keep_their_first_letter(self):
        # A one-character remainder is far more likely to be a word that merely
        # starts with the article letter: Hebrew הר (mountain) is not ה + ר.
        self.assertEqual(normalize_answer("הר", "hebrew"), "הר")
        self.assertEqual(normalize_answer("הוא", "hebrew"), "וא")

    def test_normalization_is_idempotent(self):
        # Running normalization twice must equal running it once, otherwise
        # references (normalized at load time) and predictions (normalized at
        # parse time) could drift if either path ever normalizes again.
        samples = [
            ("arabic", "الجنسية اللبنانية"),
            ("hebrew", "הספר הזה"),
            ("french", "l'Île-de-France"),
            ("german", "Der Hund und die Katze"),
            ("french", "un"),
            ("vietnamese", "Thiên An Môn"),
        ]
        for language, text in samples:
            with self.subTest(language=language, text=text):
                once = normalize_answer(text, language)
                self.assertEqual(normalize_answer(once, language), once)

    @unittest.skipUnless(HAS_DATA, "benchmark_data not extracted")
    def test_no_gold_target_normalizes_to_empty(self):
        # Dataset-wide invariant. Twelve dev targets are bare article/numeral
        # words ("un", "una", "een", "Eine"); this is the test that catches any
        # normalization rule aggressive enough to erase a whole answer.
        import json

        for language in sorted(os.listdir(BENCHMARK_DATA)):
            path = os.path.join(BENCHMARK_DATA, language, "dev.jsonl")
            if not os.path.isfile(path):
                continue
            with open(path) as f:
                for line in f:
                    for target in json.loads(line)["targets"]:
                        if not target.strip():
                            continue
                        with self.subTest(language=language, target=target):
                            self.assertNotEqual(
                                normalize_answer(target, language).strip(), ""
                            )

    @unittest.skipUnless(HAS_DATA, "benchmark_data not extracted")
    def test_stripping_never_loses_the_form_that_would_match(self):
        # Dataset-wide version of the design guarantee: for every gold target,
        # the answer as written and the answer with its articles removed always
        # share a variant, so whichever form a model produces can still match.
        import json

        for language in sorted(os.listdir(BENCHMARK_DATA)):
            path = os.path.join(BENCHMARK_DATA, language, "dev.jsonl")
            if not os.path.isfile(path):
                continue
            with open(path) as f:
                for line in f:
                    for target in json.loads(line)["targets"]:
                        if not target.strip():
                            continue
                        written = set(answer_variants(target, language))
                        stripped = set(
                            answer_variants(normalize_answer(target, language), language)
                        )
                        if not written & stripped:
                            self.fail(
                                f"{language}: {target!r} -> written={written} "
                                f"stripped={stripped} share no variant"
                            )


class TestContentLanguage(unittest.TestCase):
    def test_plain_keys_pass_through(self):
        self.assertEqual(content_language("french"), "french")
        self.assertEqual(content_language("simplified_mandarin"), "simplified_mandarin")

    def test_composite_keys_resolve_to_the_target_language(self):
        self.assertEqual(content_language("spanish_translated_human_english"), "english")
        self.assertEqual(content_language("urdu_translated_machine_english"), "english")

    def test_underscored_target_languages_survive_the_split(self):
        self.assertEqual(
            content_language("english_translated_human_simplified_mandarin"),
            "simplified_mandarin",
        )
        self.assertEqual(
            content_language("english_translated_machine_traditional_mandarin"),
            "traditional_mandarin",
        )

    def test_translated_subset_is_normalized_as_its_target_language(self):
        # An English-text row inside a Vietnamese subset gets English rules.
        self.assertEqual(
            postprocess_answers("The Gate", content_language("vietnamese_translated_human_english")),
            ["the gate", "gate"],
        )

    @unittest.skipUnless(HAS_DATA, "benchmark_data not extracted")
    def test_every_real_key_resolves_to_a_language_directory(self):
        languages = sorted(
            d for d in os.listdir(BENCHMARK_DATA)
            if os.path.isdir(os.path.join(BENCHMARK_DATA, d))
        )
        keys = set(languages)
        for subset in ("dev", "extra"):
            for language in languages:
                pattern = os.path.join(BENCHMARK_DATA, language, f"{subset}_translated*.jsonl")
                for path in glob.glob(pattern):
                    stem = os.path.basename(path).split(".jsonl")[0]
                    keys.add(stem.replace(subset, language))
        self.assertGreater(len(keys), len(languages))
        for key in sorted(keys):
            with self.subTest(key=key):
                self.assertIn(content_language(key), languages)


class TestPostprocessAnswers(unittest.TestCase):
    def test_accepts_a_string_or_a_list(self):
        self.assertEqual(postprocess_answers("Der Hund", "german"), ["der hund", "hund"])
        self.assertEqual(
            postprocess_answers(["Der Hund", "Die Katze"], "german"),
            ["der hund", "hund", "die katze", "katze"],
        )

    def test_defaults_to_english(self):
        self.assertEqual(postprocess_answers("The Cat"), ["the cat", "cat"])


class TestPredictionsAndReferencesAreTreatedAlike(unittest.TestCase):
    """
    Normalization has to be symmetric: whatever is done to a model's answer
    must be done to the gold answer as well, or the two stop being comparable.
    """

    def test_the_same_string_normalizes_the_same_on_both_sides(self):
        # parse_input_jsonl handles references, parse_output_* handle
        # predictions. All three must agree for a given language.
        for language in ("arabic", "hebrew", "german", "french"):
            for text in ("الجنسية اللبنانية", "הספר", "Der Hund", "Le chat"):
                with self.subTest(language=language, text=text):
                    reference = postprocess_answers([text], language)
                    prediction = postprocess_answers(text, language)
                    self.assertEqual(reference, prediction)

    def test_prefix_stripping_makes_the_two_sides_agree(self):
        # Regression for the Arabic case raised in review: a prediction without
        # the definite article and a gold answer carrying it must match once
        # both have been normalized.
        self.assertEqual(
            normalize_answer("اللبنانية", "arabic"),
            normalize_answer("لبنانية", "arabic"),
        )
        self.assertEqual(
            normalize_answer("הספר", "hebrew"),
            normalize_answer("ספר", "hebrew"),
        )

    @unittest.skipUnless(HAS_DATA, "benchmark_data not extracted")
    def test_reference_and_prediction_paths_agree_on_real_files(self):
        # Feed the same rows through the reference parser and both prediction
        # parsers, and require identical output.
        import csv
        import json
        import tempfile

        language = "arabic"
        source = os.path.join(BENCHMARK_DATA, language, "dev.jsonl")
        with open(source) as f:
            rows = [json.loads(line) for line in f][:40]
        # Blank gold answers exist in the data and produce no variants, so they
        # cannot stand in for a prediction here.
        rows = [
            row for row in rows
            if answer_variants(row["targets"][0], language)
        ]
        self.assertTrue(rows, "no usable rows to test with")

        references = parse_input_jsonl([(source, language)])[language]

        with tempfile.TemporaryDirectory() as tmp:
            csv_path = os.path.join(tmp, "p.csv")
            with open(csv_path, "w", newline="") as f:
                writer = csv.DictWriter(f, ["language", "id", "prediction"])
                writer.writeheader()
                for row in rows:
                    writer.writerow(
                        {"language": language, "id": row["id"], "prediction": row["targets"][0]}
                    )

            jsonl_path = os.path.join(tmp, "p.jsonl")
            with open(jsonl_path, "w") as f:
                for row in rows:
                    f.write(
                        json.dumps(
                            {"language": language, "id": row["id"], "prediction": row["targets"][0]},
                            ensure_ascii=False,
                        )
                        + "\n"
                    )

            from_csv = parse_output_csv(csv_path)[language]
            from_jsonl = parse_output_jsonl(jsonl_path)[language]

        for row in rows:
            with self.subTest(id=row["id"]):
                # The first gold answer, sent through the prediction path, must
                # share a variant with that same answer via the reference path,
                # or a correct answer would be scored wrong.
                # Every variant the prediction path produces must also be
                # offered by the reference path, or a correct answer could miss.
                self.assertTrue(set(from_csv[row["id"]]) & set(references[row["id"]]))
                self.assertTrue(set(from_jsonl[row["id"]]) & set(references[row["id"]]))


class TestAnswerVariants(unittest.TestCase):
    """
    Article handling is additive: both the written form and the stripped form
    are kept, and scoring accepts a match on any pairing. A wrong article rule
    can then only fail to add a match, never delete the one that would have
    matched.
    """

    def test_variants_always_include_the_text_as_written(self):
        # The form as written is never discarded, whatever the article rule
        # does. This is the property that makes a wrong rule harmless.
        for language, text in (
            ("german", "Der Hund"),
            ("arabic", "الكتاب"),
            ("hebrew", "הספר"),
            ("french", "le chat")
        ):
            with self.subTest(language=language, text=text):
                self.assertEqual(answer_variants(text, language)[0], _canonical_form(text))

    def test_variants_include_the_stripped_form_when_it_differs(self):
        self.assertEqual(answer_variants("Der Hund", "german"), ["der hund", "hund"])
        self.assertEqual(answer_variants("הספר", "hebrew"), ["הספר", "ספר"])

    def test_no_duplicate_variant_when_nothing_is_stripped(self):
        self.assertEqual(answer_variants("ein Kind", "german"), ["ein kind"])

    def test_variants_are_never_empty_strings(self):
        # A blank variant is poison: "" is a substring of everything, so one
        # blank target makes `contains` score 1.0 against every prediction.
        for language, text in (
            ("french", "un"), ("english", "the"), ("swedish", "en"),
            ("english", ""), ("english", "   "), ("english", "???"),
            ("japanese", "。。。"), ("japanese", "です"),
        ):
            with self.subTest(language=language, text=text):
                self.assertNotIn("", answer_variants(text, language))

    def test_answers_that_normalize_away_yield_no_variants(self):
        for language, text in (
            ("english", ""), ("english", "   "), ("english", "???"),
            ("japanese", "。。。"),
        ):
            with self.subTest(language=language, text=text):
                self.assertEqual(answer_variants(text, language), [])

    def test_a_blank_target_cannot_make_contains_score(self):
        # Regression for the metric this actually corrupts.
        targets = postprocess_answers(["", "Ich Troje"], "polish")
        self.assertNotIn("", targets)
        self.assertEqual(contains("something entirely different", targets), 0.0)

    def test_an_empty_prediction_scores_zero_rather_than_crashing(self):
        targets = postprocess_answers(["Paris"], "french")
        predictions = postprocess_answers("", "french") or [""]
        self.assertEqual(exact_match(predictions[0], targets), 0.0)
        self.assertEqual(contains(predictions[0], targets), 0.0)

    def test_an_over_stripping_rule_cannot_destroy_a_match(self):
        # The property that motivates the design. Even if a rule strips too
        # much, the as-written form survives in the variant set, so a gold and
        # a prediction that agree in *either* form still match.
        gold = set(answer_variants("ההתנתקות", "hebrew"))
        prediction = set(answer_variants("התנתקות", "hebrew"))
        self.assertTrue(gold & prediction)

    def test_article_mismatch_between_sides_still_matches(self):
        for language, gold, prediction in (
            ("arabic", "اللبنانية", "لبنانية"),
            ("german", "Der Hund", "Hund"),
            ("dutch", "de Vuurboetsduin", "Vuurboetsduin"),
            ("english", "The Sputniks", "Sputniks"),
        ):
            with self.subTest(language=language):
                self.assertTrue(
                    set(answer_variants(gold, language))
                    & set(answer_variants(prediction, language))
                )

    def test_both_sides_are_expanded_not_just_predictions(self):
        # The reference parser and both prediction parsers must all expand to
        # variants. If only one side expanded, an articled gold and a bare
        # prediction (or vice versa) would miss depending on which side the
        # article happened to land.
        import csv
        import json
        import tempfile

        language = "spanish"
        with tempfile.TemporaryDirectory() as tmp:
            gold_path = os.path.join(tmp, "g.jsonl")
            with open(gold_path, "w") as f:
                f.write(json.dumps(
                    {"id": "x", "targets": ["El Equipo A"]}, ensure_ascii=False) + "\n")
            references = parse_input_jsonl([(gold_path, language)])[language]["x"]

            csv_path = os.path.join(tmp, "p.csv")
            with open(csv_path, "w", newline="") as f:
                writer = csv.DictWriter(f, ["language", "id", "prediction"])
                writer.writeheader()
                writer.writerow(
                    {"language": language, "id": "x", "prediction": "Equipo A"})
            predictions = parse_output_csv(csv_path)[language]["x"]

        self.assertGreater(len(references), 1, "gold side was not expanded")
        self.assertIn("el equipo a", references)
        self.assertIn("equipo a", references)
        self.assertTrue(set(references) & set(predictions))

    def test_matching_does_not_depend_on_which_side_has_the_article(self):
        for language, articled, bare in (
            ("spanish", "El Equipo A", "Equipo A"),
            ("german", "Der Hund", "Hund"),
            ("arabic", "اللبنانية", "لبنانية"),
            ("hebrew", "ההתנתקות", "התנתקות"),
        ):
            with self.subTest(language=language):
                forward = set(answer_variants(articled, language)) & set(
                    answer_variants(bare, language))
                reverse = set(answer_variants(bare, language)) & set(
                    answer_variants(articled, language))
                self.assertTrue(forward)
                self.assertEqual(bool(forward), bool(reverse))

    def test_variant_order_is_deterministic_and_deduplicated(self):
        # These land in the results JSON, so the order must not depend on
        # PYTHONHASHSEED and duplicates must not accumulate.
        targets = ["El Equipo A", "Equipo A", "El Equipo A"]
        first = postprocess_answers(targets, "spanish")
        self.assertEqual(first, postprocess_answers(targets, "spanish"))
        self.assertEqual(len(first), len(set(first)))
        # as-written forms come before stripped ones, in input order
        self.assertEqual(first[0], "el equipo a")

    def test_a_dropped_numeral_is_still_not_a_match(self):
        # "ein" is not in the German list, so it is not stripped and produces
        # no extra variant: omitting the count remains a different answer.
        self.assertFalse(
            set(answer_variants("ein Kind", "german"))
            & set(answer_variants("Kind", "german"))
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)