#!/usr/bin/env python3
"""
Copyright (c) Meta Platforms, Inc. and affiliates.

This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.

Run from this directory:  python -m unittest test_prompts -v
"""
import re
import unicodedata as ud
import unittest

from prompts import FA_TOKENS, chat, fewshot, fewshot_examples
from utils import jinja_format

LOOP = re.compile(r"\{%\s*for x in few_shot.*?%\}(.*?)\{%\s*endfor.*?%\}", re.S)
JINJA_VAR = re.compile(r"\{\{\s*([^}]+?)\s*\}\}")
INDEXED_VAR = re.compile(r"\{\{\s*x\[[^\]]+\]\s*\}\}")


def loop_body(template):
    match = LOOP.search(template)
    assert match, "few-shot template has no {% for x in few_shot %} block"
    return match.group(1)


def strip_jinja(text):
    text = re.sub(r"\{\{.*?\}\}", " ", text, flags=re.S)
    return re.sub(r"\{%.*?%\}", " ", text, flags=re.S)


def is_non_latin(char):
    return ord(char) >= 128 and "LATIN" not in ud.name(char, "")


class TestTemplateStructure(unittest.TestCase):
    def test_all_dicts_cover_the_same_languages(self):
        self.assertEqual(set(fewshot), set(FA_TOKENS))
        self.assertEqual(set(chat), set(FA_TOKENS))
        self.assertEqual(set(fewshot_examples), set(FA_TOKENS))

    def test_every_language_has_five_usable_examples(self):
        for language, examples in fewshot_examples.items():
            with self.subTest(language=language):
                self.assertEqual(len(examples), 5)
                for example in examples:
                    self.assertEqual(
                        set(example), {"question", "output_type", "answer"}
                    )

    def test_every_template_renders(self):
        few = [{"question": "q", "output_type": "t", "answer": "a"}] * 5
        for name, templates in (("fewshot", fewshot), ("chat", chat)):
            for language, template in templates.items():
                with self.subTest(dict=name, language=language):
                    jinja_format(template, question="q", output_type="t", few_shot=few)


class TestDemonstrationsUseTheirOwnFields(unittest.TestCase):
    def test_loop_body_references_no_outer_variable(self):
        # Regression: Italian and Spanish referenced the outer `output_type`
        # inside the loop, so every demonstration was labelled with the query's
        # answer type instead of its own.
        for language, template in fewshot.items():
            with self.subTest(language=language):
                body = INDEXED_VAR.sub("", loop_body(template))
                self.assertEqual(
                    JINJA_VAR.findall(body),
                    [],
                    "few-shot loop must reference x[...] rather than outer variables",
                )

    def test_demonstrations_are_labelled_with_their_own_output_type(self):
        # Render with a query type that appears in no demonstration; it must not
        # leak into the demonstration lines.
        for language in ("italian", "spanish"):
            with self.subTest(language=language):
                few = fewshot_examples[language]
                rendered = jinja_format(
                    fewshot[language],
                    question="QUESTION",
                    output_type="QUERYTYPE",
                    few_shot=few,
                )
                demos = rendered.split("QUESTION")[0]
                self.assertNotIn("QUERYTYPE", demos)
                for example in few:
                    self.assertIn(example["output_type"], demos)


class TestNoStrayCharacters(unittest.TestCase):
    def test_no_latin_letter_fused_to_a_non_latin_character(self):
        # Regression: stray "c"/"d" characters sat against the surrounding
        # script in five templates and reached every generated prompt.
        for name, templates in (
            ("FA_TOKENS", FA_TOKENS),
            ("fewshot", fewshot),
            ("chat", chat),
        ):
            for language, value in templates.items():
                texts = list(value) if isinstance(value, tuple) else [value]
                for text in texts:
                    stripped = strip_jinja(text)
                    for match in re.finditer(r"[A-Za-z]", stripped):
                        i = match.start()
                        before = stripped[i - 1] if i else ""
                        after = stripped[i + 1] if i + 1 < len(stripped) else ""
                        if (before and is_non_latin(before)) or (
                            after and is_non_latin(after)
                        ):
                            self.fail(
                                f"{name}[{language!r}] has a stray {match.group()!r} "
                                f"in {stripped[max(0, i - 20):i + 10]!r}"
                            )

    def test_loop_tag_emits_nothing_of_its_own(self):
        # Regression: "{% for x in few_shot -%}c" put a bare "c" line at the top
        # of every Cantonese demonstration.
        few = [{"question": "q", "output_type": "t", "answer": "a"}] * 2
        for language, template in fewshot.items():
            with self.subTest(language=language):
                rendered = jinja_format(
                    template, question="q", output_type="t", few_shot=few
                )
                for line in rendered.split("\n"):
                    self.assertNotEqual(
                        line.strip().lower(),
                        "c",
                        "a stray character is being emitted per loop iteration",
                    )


class TestTokensMatchTemplates(unittest.TestCase):
    def test_declared_question_token_appears_in_its_template(self):
        # Regression: FA_TOKENS["khmer"] declared "សំណួរ៖c" while the template
        # used the clean "សំណួរ៖".
        for language, (question_token, _) in FA_TOKENS.items():
            with self.subTest(language=language):
                self.assertIn(question_token, fewshot[language])

    def test_cantonese_stays_in_traditional_script(self):
        # Regression: the demonstrations used 問題： and the query 问题：.
        self.assertNotIn("问题", fewshot["cantonese"])
        self.assertEqual(fewshot["cantonese"].count("問題："), 2)


class TestPunctuationConventions(unittest.TestCase):
    # Japanese takes the logographic full stop, Korean the ASCII period.
    ASCII_STOP_AFTER_CJK = re.compile(r"[ぁ-ゟ゠-ヿ一-鿿가-힣]\s*\.")

    def test_japanese_uses_the_logographic_full_stop(self):
        # Regression: the demonstration ended "ください." and the query "ください。".
        for name, templates in (("fewshot", fewshot), ("chat", chat)):
            with self.subTest(dict=name):
                self.assertEqual(
                    self.ASCII_STOP_AFTER_CJK.findall(templates["japanese"]), []
                )

    def test_korean_uses_the_ascii_period(self):
        # Regression: the query ended "대답해줘。".
        for name, templates in (("fewshot", fewshot), ("chat", chat)):
            with self.subTest(dict=name):
                self.assertNotIn("。", templates["korean"])

    def test_chinese_variants_use_the_logographic_full_stop(self):
        for language in ("simplified_mandarin", "traditional_mandarin", "cantonese"):
            for name, templates in (("fewshot", fewshot), ("chat", chat)):
                with self.subTest(language=language, dict=name):
                    self.assertEqual(
                        self.ASCII_STOP_AFTER_CJK.findall(templates[language]), []
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
