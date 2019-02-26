from lineedit.prompt import Prompt


class Completer:
    words = ["abandon", "abbey", "able", "abnormal", "abolish", "abortion", "abridge", "absence", "absent", "absolute", "absorb", "absorption", "abstract", "abundant", "abuse", "academy", "accent", "accept", "acceptable", "acceptance", "access", "accessible", "accident", "accompany", "account", "accountant", "accumulation", "accurate", "achieve", "achievement", "acid", "acquaintance", "acquisition", "acquit", "act", "action", "activate", "active", "activity", "acute", "add", "addicted", "addition", "address", "adjust", "administration", "admiration", "admire", "admission", "admit", "adopt", "adoption", "adult", "advance", "advantage", "adventure", "advertise", "advertising", "advice", "adviser", "advocate", "affair", "affect", "affinity", "afford", "age", "agency", "agenda", "agent", "agile", "agony", "agree", "agreement", "agriculture", "aid", "AIDS", "air", "aisle", "alarm", "album", "alcohol", "alive", "allocation", "allow", "allowance", "ally", "aloof", "aluminium", "amber", "ambiguity", "ambiguous", "ambition", "ample", "amputate", "amuse", "analysis", "analyst", "ancestor", "angel", "anger", "angle", "animal", "ankle", "anniversary", "announcement", "annual", "answer", "ant", "anticipation", "anxiety", "apathy", "apology", "apparatus", "appeal", "appear", "appearance", "appendix", "appetite", "applaud", "apple", "application", "applied", "appoint", "appointment", "appreciate", "approach", "approval", "approve", "aquarium", "arch", "architect", "architecture", "archive", "area", "arena", "argument", "arise", "arm", "army", "arrange", "arrangement", "arrest", "arrogant", "arrow", "art", "article", "articulate", "artificial", "artist", "ash", "ask", "aspect", "assault", "assembly", "assertive", "assessment", "asset", "assignment", "association", "assume", "assumption", "astonishing", "asylum", "athlete", "atmosphere", "attachment", "attack", "attention", "attic", "attitude", "attract", "attraction", "attractive", "auction", "audience", "auditor", "aunt", "authorise", "authority", "automatic", "autonomy", "available", "avant-garde", "avenue", "average", "aviation", "award", "aware", "awful", "axis"]

    def get_completions(self, document):
        text_before_cursor = document.text_before_cursor
        for word in self.words:
            if word.startswith(text_before_cursor):
                yield (word, -len(text_before_cursor))


p = Prompt("> ", completer=Completer())
p.run()
print("we get " + p.value)
