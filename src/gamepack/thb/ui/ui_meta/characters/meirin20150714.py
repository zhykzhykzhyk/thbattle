# -*- coding: utf-8 -*-

# -- stdlib --
# -- third party --
# -- own --
from gamepack.thb import characters
from gamepack.thb.actions import ttags
from gamepack.thb.ui.ui_meta.common import gen_metafunc, my_turn


# -- code --
__metaclass__ = gen_metafunc(characters.meirin20150714)


class Qiliao:
    # Skill
    name = u'气疗'

    def clickable(g):
        if not my_turn():
            return False

        if ttags(g.me)['qiliao']:
            return False

        return True

    def is_action_valid(g, cl, target_list):
        skill = cl[0]
        n = len([p for p in g.players if not p.dead]) / 2
        if not 0 < len(skill.associated_cards) <= n:
            return False, u'气疗：请选择至多%s张牌放置在人物牌上' % n

        return True, u'发动气疗'

    def effect_string(act):
        # for LaunchCard.ui_meta.effect_string
        return u'|G【%s】|r发动了|G气疗|r' % act.source.ui_meta.char_name


class QiliaoDropHandler:

    def choose_card_text(g, act, cl):
        if act.cond(cl):
            return (True, u'弃置弹幕并弃置一张气')
        else:
            return (False, u'气疗：弃置弹幕并弃置一张气（否则开始出牌）')


class QiliaoRecoverHandler:

    def target(pl):
        if not pl:
            return (False, u'请选择1名玩家发动气疗效果（否则不发动）')

        return (True, u'发动气疗效果')


class Meirin20150714:
    # Character
    char_name = u'红美铃'
    port_image = 'thb-portrait-meirin20150714'
    description = (
        u'|DB华人小娘 红美铃 体力：4|r\n\n'
        u'|G气疗|r：出牌阶段限一次，你可以将至多X张牌背面朝上置于你的武将牌上，称为“气”。其他角色的出牌阶段开始时，该角色可以弃置一张|G弹幕|r，将一张“气”置入弃牌堆。你的回合开始时，若你有“气”，你令一名角色获得所有“气”并令其回复1点体力。（X为当前存活角色数的一半，向下取整）\n\n'
        u'|DB（人物设计：罗妲.坂井）|r'
    )
