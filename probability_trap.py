from manim import *
import numpy as np


class PositiveTestParadox(Scene):
    def make_population(self):
        dots = VGroup()
        rows = 20
        cols = 50

        for i in range(rows):
            for j in range(cols):
                dot = Dot(radius=0.032, color=GRAY)
                dot.move_to(np.array([-5.9 + j * 0.24, 1.55 - i * 0.16, 0]))
                dots.add(dot)

        return dots

    def make_legend(self):
        legend_items = VGroup(
            VGroup(Dot(color=GREEN), Text("9 true positives", font_size=24)),
            VGroup(Dot(color=RED), Text("1 missed case", font_size=24)),
            VGroup(Dot(color=YELLOW), Text("50 false positives", font_size=24)),
            VGroup(Dot(color=GRAY), Text("940 true negatives", font_size=24)),
        )

        for item in legend_items:
            item.arrange(RIGHT, buff=0.22)

        legend_items.arrange_in_grid(rows=2, cols=2, buff=(1.6, 0.38))
        legend_items.to_edge(DOWN, buff=0.35)
        return legend_items

    def construct(self):
        title = Text("The Positive Test Paradox", font_size=44)
        subtitle = Text("A probability lesson hiding in one surprising question", font_size=26)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        hook1 = Text("A medical test is very accurate.", font_size=38)
        hook2 = Text("You test positive.", font_size=42, color=YELLOW)
        hook3 = Text("What are the chances you actually have the condition?", font_size=30)

        hook2.next_to(hook1, DOWN, buff=0.45)
        hook3.next_to(hook2, DOWN, buff=0.45)

        self.play(Write(hook1))
        self.play(Write(hook2))
        self.play(Write(hook3))
        self.wait(2.5)
        self.play(FadeOut(hook1), FadeOut(hook2), FadeOut(hook3))

        dots = self.make_population()

        population_label = Text("Start with 1,000 people", font_size=40)
        population_label.to_edge(UP, buff=0.22)

        self.play(Write(population_label))
        self.play(
            LaggedStart(*[FadeIn(dot) for dot in dots], lag_ratio=0.0005),
            run_time=2,
        )
        self.wait(1)

        sick = VGroup(*dots[:10])
        true_positive = VGroup(*dots[:9])
        false_negative = dots[9]
        false_positive = VGroup(*dots[10:60])

        prevalence_label = Text("Only 10 actually have the condition", font_size=34, color=RED)
        prevalence_label.next_to(population_label, DOWN, buff=0.22)

        self.play(sick.animate.set_color(RED), Write(prevalence_label), run_time=1.5)
        self.wait(1.3)

        tp_label = Text("The test catches 9 of the 10", font_size=30, color=GREEN)
        tp_label.to_edge(DOWN, buff=1.35)

        self.play(
            true_positive.animate.set_color(GREEN),
            false_negative.animate.set_color(RED),
            Write(tp_label),
            run_time=1.3,
        )
        self.wait(1.3)

        fp_label = Text("But it also flags 50 healthy people", font_size=30, color=YELLOW)
        fp_label.next_to(tp_label, DOWN, buff=0.22)

        self.play(false_positive.animate.set_color(YELLOW), Write(fp_label), run_time=1.5)
        self.wait(1.6)

        legend = self.make_legend()

        self.play(FadeOut(tp_label), FadeOut(fp_label), run_time=0.7)
        self.play(FadeIn(legend), run_time=1)
        self.wait(2)

        self.play(FadeOut(legend), run_time=0.7)

        positive_tests = VGroup(*dots[:9], *dots[10:60])
        not_positive = VGroup(*[dot for dot in dots if dot not in positive_tests])

        transition = Text("Now only look at the people who tested positive.", font_size=30)
        transition.to_edge(DOWN, buff=0.35)

        self.play(Write(transition))
        self.wait(1.3)

        self.play(
            FadeOut(not_positive),
            FadeOut(population_label),
            FadeOut(prevalence_label),
            FadeOut(transition),
            positive_tests.animate.arrange_in_grid(rows=5, cols=12, buff=0.16).move_to(UP * 0.8),
            run_time=2.5,
        )

        positive_label = Text("59 positive tests", font_size=38)
        positive_label.to_edge(UP, buff=0.35)

        self.play(Write(positive_label))
        self.wait(1)

        true_group = VGroup(*positive_tests[:9])
        false_group = VGroup(*positive_tests[9:])

        brace_true = Brace(true_group, UP, color=GREEN)
        true_text = Text("9 true positives", font_size=24, color=GREEN)
        true_text.next_to(brace_true, UP, buff=0.12)

        brace_false = Brace(false_group, DOWN, color=YELLOW)
        false_text = Text("50 false positives", font_size=24, color=YELLOW)
        false_text.next_to(brace_false, DOWN, buff=0.12)

        self.play(GrowFromCenter(brace_true), Write(true_text))
        self.play(GrowFromCenter(brace_false), Write(false_text))
        self.wait(2)

        self.play(
            FadeOut(brace_true),
            FadeOut(brace_false),
            FadeOut(true_text),
            FadeOut(false_text),
        )

        reveal = Text("So the chance is not 90%.", font_size=34)
        reveal2 = Text("It is 9 out of 59.", font_size=36, color=GREEN)
        reveal_group = VGroup(reveal, reveal2).arrange(DOWN, buff=0.35)
        reveal_group.to_edge(DOWN, buff=0.55)

        self.play(Write(reveal))
        self.play(Write(reveal2))
        self.wait(1.5)

        percent = Text("9 / 59 ≈ 15%", font_size=56, color=GREEN)
        percent.to_edge(DOWN, buff=0.75)

        self.play(Transform(reveal_group, percent))
        self.wait(2.5)

        self.play(FadeOut(positive_tests), FadeOut(positive_label), FadeOut(reveal_group))

        bayes_title = Text("This is Bayes' theorem.", font_size=42)
        bayes_title.to_edge(UP, buff=0.45)

        bayes_formula = Text(
            "P(condition | positive) = [P(positive | condition) × P(condition)] / P(positive)",
            font_size=24,
        )
        bayes_formula.next_to(bayes_title, DOWN, buff=0.55)

        context1 = Text("In this story, we want P(condition | positive):", font_size=28)
        context2 = Text(
            "the chance someone has the condition, given that they tested positive.",
            font_size=26,
            color=YELLOW,
        )

        context_group = VGroup(context1, context2).arrange(DOWN, buff=0.28)
        context_group.next_to(bayes_formula, DOWN, buff=0.7)

        numerator = Text(
            "The numerator counts true positives: people with the condition who test positive.",
            font_size=24,
            color=GREEN,
        )

        denominator = Text(
            "The denominator counts all positives: true positives plus false positives.",
            font_size=24,
            color=YELLOW,
        )

        numerator.next_to(context_group, DOWN, buff=0.65)
        denominator.next_to(numerator, DOWN, buff=0.35)

        example = Text(
            "So here: 9 true positives / 59 positive tests ≈ 15%.",
            font_size=30,
            color=GREEN,
        )
        example.next_to(denominator, DOWN, buff=0.65)

        self.play(Write(bayes_title))
        self.play(Write(bayes_formula))
        self.play(Write(context1), Write(context2))
        self.wait(1)
        self.play(Write(numerator))
        self.play(Write(denominator))
        self.play(Write(example))
        self.wait(4)

        self.play(
            FadeOut(bayes_title),
            FadeOut(bayes_formula),
            FadeOut(context_group),
            FadeOut(numerator),
            FadeOut(denominator),
            FadeOut(example),
        )

        lesson1 = Text("Bayes' theorem is about changing the denominator.", font_size=34)
        lesson2 = Text("We do not only ask: How accurate is the test?", font_size=28)
        lesson3 = Text("We ask: Among the positives, how many are real?", font_size=30, color=YELLOW)

        lesson_group = VGroup(lesson1, lesson2, lesson3).arrange(DOWN, buff=0.5)

        self.play(Write(lesson1))
        self.play(Write(lesson2))
        self.play(Write(lesson3))
        self.wait(3)

        self.play(FadeOut(lesson_group))

        final = Text("Evidence matters.", font_size=42)
        final2 = Text("But base rates matter too.", font_size=42, color=YELLOW)
        final2.next_to(final, DOWN)

        self.play(Write(final))
        self.play(Write(final2))
        self.wait(3)
