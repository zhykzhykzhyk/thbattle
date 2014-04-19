# -*- coding: utf-8 -*-

from gamepack.thb import actions
from gamepack.thb import cards
from gamepack.thb import characters
from gamepack.thb.ui.ui_meta.common import gen_metafunc
from gamepack.thb.ui.ui_meta.common import passive_clickable, passive_is_action_valid
from gamepack.thb.ui.ui_meta.common import limit1_skill_used
from gamepack.thb.ui.resource import resource as gres

__metaclass__ = gen_metafunc(characters.alice)


class Alice:
    # Character
    char_name = u'爱丽丝'
    port_image = gres.alice_port
    description = (
        u'|DB七色的人偶使 爱丽丝 体力：3|r\n\n'
        u'|G小小军势|r：当你使用装备牌时，你可以摸一张牌。当你失去装备牌区的牌后，你可以弃置其它角色的一张牌。\n\n'
        u'|G少女文乐|r：锁定技，你的手牌上限+X（X为你装备区牌数量的一半，向上取整且至少为1）。'
    )


class LittleLegion:
    # Skill
    name = u'小小军势'
    clickable = passive_clickable
    is_action_valid = passive_is_action_valid


class LittleLegionDrawCards:
    pass


class LittleLegionAction:
    def effect_string(act):
        return u'|G【%s】|r对|G【%s】|r发动了|G小小军势|r。' % (
            act.source.ui_meta.char_name,
            act.target.ui_meta.char_name
        )


class LittleLegionHandler:
    choose_option_buttons = ((u'发动', True), (u'不发动', False))
    choose_option_prompt = u'你要发动【小小军势】吗？'

    def target(tl):
        if not tl:
            return False, u'小小军势：弃置目标的一张牌'

        tgt = tl[0]

        if tgt.cards or tgt.showncards or tgt.equips:
            return True, u'让你见识一下这人偶军团的厉害！'
        else:
            return False, u'这货已经没有牌了'


class MaidensBunraku:
    # Skill
    name = u'少女文乐'
    clickable = passive_clickable
    is_action_valid = passive_is_action_valid

# ----------
