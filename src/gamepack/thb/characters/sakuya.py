# -*- coding: utf-8 -*-

# -- stdlib --
# -- third party --
# -- own --
from game.autoenv import EventHandler
from gamepack.thb.actions import ActionStage, PlayerTurn, PrepareStage
from gamepack.thb.cards import AttackCard, Skill, TreatAs, t_None
from gamepack.thb.characters.baseclasses import Character, register_character


# -- code --
class Dagger(TreatAs, Skill):
    skill_category = ('character', 'active')
    treat_as = AttackCard
    distance = 99999

    def check(self):
        cards = self.associated_cards
        if len(cards) != 1:
            return False

        c = cards[0]
        if c.resides_in is None:
            return False

        if c.resides_in.type not in ('cards', 'showncards', 'equips'):
            return False

        if 'equipment' not in c.category:
            return False

        return True


class LunaDialActionStage(ActionStage):
    def apply_action(self):
        tags = self.target.tags
        tags['lunadial'] = True

        try:
            return super(LunaDialActionStage, self).apply_action()
        finally:
            tags['lunadial'] = False


class LunaDial(Skill):
    associated_action = None
    skill_category = ('character', 'passive', 'compulsory')
    target = t_None


class LunaDialHandler(EventHandler):
    interested = ('action_after',)
    execute_after = ('CiguateraHandler', )

    def handle(self, evt_type, act):
        if evt_type == 'action_after' and isinstance(act, PrepareStage):
            src = act.target
            if not src.has_skill(LunaDial):
                return act

            PlayerTurn.get_current(src).pending_stages.insert(0, LunaDialActionStage)

        return act


@register_character
class Sakuya(Character):
    skills = [Dagger, LunaDial]
    eventhandlers_required = [LunaDialHandler]
    maxlife = 4
