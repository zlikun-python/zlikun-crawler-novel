#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zlikun
import asyncio

import aiohttp
from downloader import download
from pyquery import PyQuery


async def parse_chapter(html, url):
    """
    章节正文解析器

    :param html:
    :param url:
    :return: ($title, $content, $url)
    """
    if not html or not url:
        return
    pq = PyQuery(html, url=url)
    title = pq('div.bookname > h1').text().strip()
    content = content_filter(pq('#content').text().strip())
    return title, content, url


def content_filter(content):
    """
    章节正文过滤器

    :param content:
    :return:
    """
    content = content.replace("&nbsp;", " ")
    return content


async def parse_catalog(html, url, flag_url=None):
    """
    章节列表解析器

    :param html: 要解析的网页正文
    :param url: 要解析的网页URL
    :param flag_url: 用于过滤已处理过URL的标记URL，按顺序遍历章节列表，取该标记之后（不包含flag_url）的URL
    :return: [(id, url), (id, url), ...]
    """
    pq = PyQuery(html, url=url)

    # 提取章节列表
    chapters = []
    flag = False
    for i, e in enumerate(pq('#list dd > a').items()):
        # 忽略前九项，是该站的最新章节，与下面的章节列表有重复
        if i < 9:
            continue
        href = e.attr('href').strip()
        if flag_url is not None:
            # 使用flag标记控制新加入的章节列表
            if flag:
                chapters.append((i - 8, href))
            # 直到与flag_url相等，才开始计（不包含）
            if href == flag_url:
                flag = True
        else:
            chapters.append((i - 8, href))

    return chapters


async def parse_novel_page(html, url):
    """
    解析小说主页（章节列表页，但提取的是小说相关数据）

    :param html: 要解析的网页正文
    :param url: 要解析的网页URL
    :return:
    """
    pq = PyQuery(html, url=url)

    name = pq("#info > h1").text().strip()
    author = pq("#info > p:eq(0)").text().replace("作\xa0\xa0\xa0\xa0者：", "").strip()
    cover = pq("#fmimg > img").attr("src")

    return {
        "name": name,
        "author": author,
        "cover": cover,
        "catalog_url": url
    }


async def testing():
    async with aiohttp.ClientSession() as session:
        # 章节列表页
        url = "https://www.biquge5200.cc/52_52542/"
        html = await download(session, url)

        # 测试解析章节列表
        catalog_data = await parse_catalog(html, url, 'https://www.biquge5200.cc/52_52542/158470791.html')
        # [(1253, 'https://www.biquge5200.cc/52_52542/158490694.html'), (1254, 'https://www.biquge5200.cc/52_52542/158542410.html')]
        print(catalog_data)

        # 测试解析小说信息
        novel_data = await parse_novel_page(html, url)
        # {'name': '圣墟', 'author': '辰东', 'cover': 'http://r.m.biquge5200.cc/cover/aHR0cDovL3FpZGlhbi5xcGljLmNuL3FkYmltZy8zNDk1NzMvMTAwNDYwODczOC8xODA=', 'catalog_url': 'https://www.biquge5200.cc/52_52542/'}
        print(novel_data)

        # 章节正文页
        url = "https://www.biquge5200.cc/52_52542/20380548.html"
        html = await download(session, url)

        # 测试解析章节正文
        chapter_data = await parse_chapter(html, url)
        # ('第一章 沙漠中的彼岸花', '大漠孤烟直，长河落日圆。\n一望无垠的大漠，空旷而高远，壮阔而雄浑，当红日西坠，地平线尽头一片殷红，磅礴中亦有种苍凉感。\n上古的烽烟早已在岁月中逝去，黄河古道虽然几经变迁，但依旧在。\n楚风一个人在旅行，很疲惫，他躺在黄沙上，看着血色的夕阳，不知道还要多久才能离开这片大漠。\n数日前他毕业了，同时也跟校园中的女神说再见，或许见不到了吧，毕竟他曾被委婉的告知，从此天各一方，该分手了。\n离开学院后，他便出来旅行。\n落日很红，挂在大漠的尽头，在空旷中有一种宁静的美。\n楚风坐起来喝了一些水，感觉精力恢复了不少，他的身体属于修长强健那一类型，体质非常好，疲惫渐消退。\n站起来眺望，他觉得快要离开大漠了，再走一段路程或许就会见到牧民的帐篷，他决定继续前行。\n一路西进，他在大漠中留下一串很长、很远的脚印。\n无声无息，竟起雾了，这在沙漠中非常罕见。\n楚风惊讶，而这雾竟然是蓝色的，在这深秋季节给人一种凉意。\n不知不觉间，雾霭渐重，蓝色缭绕，朦朦胧胧，笼罩了这片沙漠。\n大漠尽头，落日都显得有些诡异了，渐渐化成一轮蓝日，有种魔性的美，而火云也被染成了蓝色。\n楚风皱眉，虽然他知道，沙漠的天气最是多变，但眼前实在不太正常。\n一片寂静，他停下脚步。\n在进大漠前，他曾听当地的老牧民讲过，一个人走在沙漠中，有时会听到一些古怪的声音，会见到一些奇异的东西，要格外谨慎。\n当时他并未在意。\n依旧宁静，沙漠中除却多了一层朦胧的蓝雾，并没有其他变故发生，楚风加快脚步，他想尽快离开这里。\n大漠的尽头，落日蓝的妖异，染蓝了西部的天空，不过它终究快要消失在地平线上了。\n楚风的速度越来越快，开始奔跑，他不想呆在这种诡异、充满不确定性的地方。\n在沙漠中，海市蜃楼那样的奇景多发生在烈日当空下，眼下不相符，这不像是什么蜃景。\n突然，前面传来轻响，像是有什么东西破沙而出，而且声音很密集，此起彼伏。\n楚风倏地停下脚步，盯着沙漠，前方地面蓝光星星点点，像是散落一地蓝钻，晶莹透亮，在落日的余晖中闪耀着。\n那是一棵又一棵嫩苗，不足一寸高，自沙漠中破土而出，带着美丽的光泽，剔透而妖异，遍地皆是。\n短暂的停滞，随后沙沙声成片，蓝色灿灿，所有嫩苗都快速拔高，一瞬间生长起来。\n天边，蓝日下沉，即将消失，雾气弥漫，浩瀚的大漠如同披上了一层诡异的蓝色薄纱。\n“啵！”\n花朵绽放的声音传出，沙漠中一片湛蓝，在夕阳即将消失的刹那，这些植物开始绽放出成片的花朵。\n大量的蓝花，晶莹点点，犹若梦幻，有些醉人，遍开在沙漠中，非常不真实。\n这种植物一尺多高，通体如蓝珊瑚般透亮，花瓣一条条，妖艳而迷人，宛若盛放在另一片国度，带着魔性，吸引人的心神。\n楚风退后一步，然而，身后也已满是这种植物，蓝光流动，一眼望不到边。\n他很吃惊，仔细的看着，努力辨认，这像极了彼岸花，一条条花瓣展开，又向后弯曲，极其美丽。\n不过，彼岸花红的鲜艳，而它却是蓝色的，从未听闻有蓝色彼岸花。\n彼岸花真实存在，带着浓烈的宗教色彩，关于它有太多的传说，但楚风不信这些，只为眼前的景象而惊。\n沙漠干燥、缺水，只有极其稀少的耐旱植物偶尔可见，零星散落着。而彼岸花喜欢阴森、潮湿的环境，无论如何也不该在这里出现，还如此的妖艳。\n这里遍地都是，一眼望不到尽头。\n大漠浩瀚，薄雾染蓝了落日，浸透了天边，而整片空旷无垠的沙漠都生出蓝色的彼岸花，说不出的奇异、神秘！\n一缕淡淡的芬芳飘漾，让人沉迷。\n楚风用力摇头，小心的迈步，避开这些花，他发现只有一个地带没有这种植物，那就是———黄河古道。\n在岁月中多次变迁，几经改道，它贯穿这片大漠，如今已近干涸，蓝色彼岸花开遍两岸，拥簇着它。\n花开两岸，彼此遥见。\n终于，太阳沉下去了，而也正是在此时，这些植物盛放，花开到极致，化作蓝色的海洋，流光溢彩。\n虽然暮色降临，但这里蓝色光泽缭绕，极致炫目，艳丽的出奇。\n楚风站在黄河古道上，心中无法宁静，但是他却不作停留，沿河道快速前进。\n天色渐暗，最后的落日余晖也已不见了。\n蓝色的大漠光彩点点，而后突然间，砰然一声，所有蓝色彼岸花怒放后，竟然在一瞬间同时凋零。\n妖艳的花瓣枯萎，接着整株的植物开始干枯，它们失去色彩，耗尽生机，迅速发黄，而后碎裂，像是在一瞬间失去了数十年。\n“砰！”\n最后的刹那，遍地干枯的蓝色彼岸花寸寸断裂，化成了粉末。\n这诡异的景象，很难解释。\n它们如同烟花般，短暂的绚烂，美丽到极致，而后便凋零，成为灰烬。\n枯黄的粉末落在沙地间，在暮色中很难辨出，而此时蓝雾也早已消失，大漠恢复了原样，像是什么都不曾发生过，再次宁静。\n楚风没有驻足，大步前行，在暮色中，他翻过许多座沙丘，终于见到了地平线上的山影，要离开大漠了。\n天色渐黑，他终于走出来了，清晰的看到了山地，也隐约间看到了山脚下牧民的帐篷。\n再回头时，身后大漠浩瀚，很寂静，跟平日没什么两样。\n山地前方，灯火摇曳，离山脚下还较远时就听到了一些嘈杂声，那里不平静，像是有什么事情正在发生。\n此外，还有牛羊等牲畜惶恐的叫声，以及藏獒沉闷的低吼声。\n有异常之事吗？楚风加快脚步，赶到山脚下，临近牧民的栖居地。', 'https://www.biquge5200.cc/52_52542/20380548.html')
        print(chapter_data)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(testing())
    loop.close()

    # 测试过滤器
    # 大漠孤烟直，    长河落日圆。    一望无垠的大漠，...
    print(content_filter("大漠孤烟直，&nbsp;&nbsp;&nbsp;&nbsp;长河落日圆。&nbsp;&nbsp;&nbsp;&nbsp;一望无垠的大漠，..."))
