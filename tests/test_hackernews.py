# This file is placed in the Public Domain.
#
#
# pylint: disable=C,R,W1503


"no tests"


import unittest


from rssbot.modules.rss import Parser


class TestParse(unittest.TestCase):

    def test_hnrss(self):
        res = Parser.parse(TXT)
        self.assertEqual(len(res), 20)
        

TXT = """
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>Hacker News: Newest</title><link>https://news.ycombinator.com/newest</link><description>Hacker News RSS</description><docs>https://hnrss.org/</docs><generator>hnrss v2.1.1</generator><lastBuildDate>Mon, 11 Mar 2024 19:18:15 +0000</lastBuildDate><atom:link href="https://hnrss.org/newest" rel="self" type="application/rss+xml"/><item><title><![CDATA[CISA forced to take two systems offline last month after Ivanti compromise]]></title><description><![CDATA[
<p>Article URL: <a href="https://therecord.media/cisa-takes-two-systems-offline-following-ivanti-compromise">https://therecord.media/cisa-takes-two-systems-offline-following-ivanti-compromise</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672201">https://news.ycombinator.com/item?id=39672201</a></p>
<p>Points: 1</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 19:15:29 +0000</pubDate><link>https://therecord.media/cisa-takes-two-systems-offline-following-ivanti-compromise</link><dc:creator>mooreds</dc:creator><comments>https://news.ycombinator.com/item?id=39672201</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672201</guid></item><item><title><![CDATA[Making Open Source form management tool for developers. What do you think?]]></title><description><![CDATA[
<p>Article URL: <a href="https://phpform.dev/">https://phpform.dev/</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672188">https://news.ycombinator.com/item?id=39672188</a></p>
<p>Points: 1</p>
<p># Comments: 1</p>
]]></description><pubDate>Mon, 11 Mar 2024 19:14:52 +0000</pubDate><link>https://phpform.dev/</link><dc:creator>avshelestov</dc:creator><comments>https://news.ycombinator.com/item?id=39672188</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672188</guid></item><item><title><![CDATA[Test Web Bluetooth with Puppeteer]]></title><description><![CDATA[
<p>Article URL: <a href="https://developer.chrome.com/blog/test-web-bluetooth-with-puppeteer">https://developer.chrome.com/blog/test-web-bluetooth-with-puppeteer</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672170">https://news.ycombinator.com/item?id=39672170</a></p>
<p>Points: 1</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 19:12:53 +0000</pubDate><link>https://developer.chrome.com/blog/test-web-bluetooth-with-puppeteer</link><dc:creator>fagnerbrack</dc:creator><comments>https://news.ycombinator.com/item?id=39672170</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672170</guid></item><item><title><![CDATA[Leading an Effective Design OrganizationFeatured]]></title><description><![CDATA[
<p>Article URL: <a href="https://elpha.com/posts/utm0ffh4/leading-an-effective-design-organization">https://elpha.com/posts/utm0ffh4/leading-an-effective-design-organization</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672152">https://news.ycombinator.com/item?id=39672152</a></p>
<p>Points: 1</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 19:10:20 +0000</pubDate><link>https://elpha.com/posts/utm0ffh4/leading-an-effective-design-organization</link><dc:creator>mooreds</dc:creator><comments>https://news.ycombinator.com/item?id=39672152</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672152</guid></item><item><title><![CDATA[Ask HN: Are AI and data centers are worth the amount of power they use?]]></title><description><![CDATA[
<p>Amazon recently bought a data center in Pennsylvania that comes with a guaranteed 960 MW of power. 
(See https://www.datacenterdynamics.com/en/news/aws-acquires-talens-nuclear-data-center-campus-in-pennsylvania/)<p>That one building will consume more power than any city in the US except Miami. More than New York, more than Houston or Chicago or LA! (See https://www.statista.com/statistics/807951/average-monthly-electricity-usage-in-major-us-cities/ for stats on power usage by US cities.)<p>Today, the Washington Post reports that US power utilities don't know how they're going to meet demand for new data centers in the coming years. They can't build infrastructure fast enough. (Non-paywalled version of Post article: https://archive.is/xmQTg)<p>We're at the point where a single data center can offset the gains of entire cities switching to LEED certified buildings and energy-efficient bulbs and appliances.<p>The SaaS products we develop now consume a lot of power because they have redundancy across all components. AI uses massive amounts of power for its fundamental operations.<p>Given all this, is anyone questioning whether the software and AI we're developing is even worth this level of power consumption? Could that energy be better spent elsewhere?</p>
<hr>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672148">https://news.ycombinator.com/item?id=39672148</a></p>
<p>Points: 2</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 19:09:44 +0000</pubDate><link>https://news.ycombinator.com/item?id=39672148</link><dc:creator>diamondap</dc:creator><comments>https://news.ycombinator.com/item?id=39672148</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672148</guid></item><item><title><![CDATA[Spacesuit integrated carbon nanotube dust ejection/removal system]]></title><description><![CDATA[
<p>Article URL: <a href="https://www.sciencedirect.com/science/article/abs/pii/S2468896721000987">https://www.sciencedirect.com/science/article/abs/pii/S2468896721000987</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672146">https://news.ycombinator.com/item?id=39672146</a></p>
<p>Points: 2</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 19:09:40 +0000</pubDate><link>https://www.sciencedirect.com/science/article/abs/pii/S2468896721000987</link><dc:creator>mooreds</dc:creator><comments>https://news.ycombinator.com/item?id=39672146</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672146</guid></item><item><title><![CDATA[Interactive Mapping of 1800 GPT responses]]></title><description><![CDATA[
<p>Article URL: <a href="https://artificial-worldviews.kimalbrecht.com/">https://artificial-worldviews.kimalbrecht.com/</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672142">https://news.ycombinator.com/item?id=39672142</a></p>
<p>Points: 1</p>
<p># Comments: 1</p>
]]></description><pubDate>Mon, 11 Mar 2024 19:09:32 +0000</pubDate><link>https://artificial-worldviews.kimalbrecht.com/</link><dc:creator>heroldhadanas</dc:creator><comments>https://news.ycombinator.com/item?id=39672142</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672142</guid></item><item><title><![CDATA[The later we meet someone in a sequence, the more negatively we describe them]]></title><description><![CDATA[
<p>Article URL: <a href="https://suchscience.org/people-encountered-later-in-a-sequence-described-more-negatively/">https://suchscience.org/people-encountered-later-in-a-sequence-described-more-negatively/</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672111">https://news.ycombinator.com/item?id=39672111</a></p>
<p>Points: 2</p>
<p># Comments: 1</p>
]]></description><pubDate>Mon, 11 Mar 2024 19:05:40 +0000</pubDate><link>https://suchscience.org/people-encountered-later-in-a-sequence-described-more-negatively/</link><dc:creator>amichail</dc:creator><comments>https://news.ycombinator.com/item?id=39672111</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672111</guid></item><item><title><![CDATA[GitHub Status – Incident with Actions]]></title><description><![CDATA[
<p>Article URL: <a href="https://www.githubstatus.com/incidents/bgnqgwyj76l4">https://www.githubstatus.com/incidents/bgnqgwyj76l4</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672106">https://news.ycombinator.com/item?id=39672106</a></p>
<p>Points: 1</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 19:05:03 +0000</pubDate><link>https://www.githubstatus.com/incidents/bgnqgwyj76l4</link><dc:creator>enescakir</dc:creator><comments>https://news.ycombinator.com/item?id=39672106</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672106</guid></item><item><title><![CDATA[The z/Architecture Principles of Operation [pdf]]]></title><description><![CDATA[
<p>Article URL: <a href="https://www.ibm.com/docs/en/SSQ2R2_15.0.0/com.ibm.tpf.toolkit.hlasm.doc/dz9zr006.pdf">https://www.ibm.com/docs/en/SSQ2R2_15.0.0/com.ibm.tpf.toolkit.hlasm.doc/dz9zr006.pdf</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672093">https://news.ycombinator.com/item?id=39672093</a></p>
<p>Points: 1</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 19:03:23 +0000</pubDate><link>https://www.ibm.com/docs/en/SSQ2R2_15.0.0/com.ibm.tpf.toolkit.hlasm.doc/dz9zr006.pdf</link><dc:creator>gjvc</dc:creator><comments>https://news.ycombinator.com/item?id=39672093</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672093</guid></item><item><title><![CDATA[AI's Effect on Human Consciousness]]></title><description><![CDATA[
<p>Article URL: <a href="https://wowana.me/blog/ais-effect-on-human-consciousness.xht">https://wowana.me/blog/ais-effect-on-human-consciousness.xht</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672083">https://news.ycombinator.com/item?id=39672083</a></p>
<p>Points: 1</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 19:02:10 +0000</pubDate><link>https://wowana.me/blog/ais-effect-on-human-consciousness.xht</link><dc:creator>airhangerf15</dc:creator><comments>https://news.ycombinator.com/item?id=39672083</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672083</guid></item><item><title><![CDATA[LLMs become more covertly racist with human intervention]]></title><description><![CDATA[
<p>Article URL: <a href="https://www.technologyreview.com/2024/03/11/1089683/llms-become-more-covertly-racist-with-human-intervention/">https://www.technologyreview.com/2024/03/11/1089683/llms-become-more-covertly-racist-with-human-intervention/</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672046">https://news.ycombinator.com/item?id=39672046</a></p>
<p>Points: 1</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 18:59:17 +0000</pubDate><link>https://www.technologyreview.com/2024/03/11/1089683/llms-become-more-covertly-racist-with-human-intervention/</link><dc:creator>cdme</dc:creator><comments>https://news.ycombinator.com/item?id=39672046</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672046</guid></item><item><title><![CDATA[Apple is reportedly testing an AI-powered ads product]]></title><description><![CDATA[
<p>Article URL: <a href="https://invezz.com/news/2024/03/11/apple-testing-ai-powered-ads-product/">https://invezz.com/news/2024/03/11/apple-testing-ai-powered-ads-product/</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672026">https://news.ycombinator.com/item?id=39672026</a></p>
<p>Points: 2</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 18:57:33 +0000</pubDate><link>https://invezz.com/news/2024/03/11/apple-testing-ai-powered-ads-product/</link><dc:creator>pg_1234</dc:creator><comments>https://news.ycombinator.com/item?id=39672026</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672026</guid></item><item><title><![CDATA[Reddit's planned IPO share price seems high, unless you look at its AI revenue]]></title><description><![CDATA[
<p>Article URL: <a href="https://techcrunch.com/2024/03/11/reddit-ipo-share-price-plans/">https://techcrunch.com/2024/03/11/reddit-ipo-share-price-plans/</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672021">https://news.ycombinator.com/item?id=39672021</a></p>
<p>Points: 1</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 18:57:00 +0000</pubDate><link>https://techcrunch.com/2024/03/11/reddit-ipo-share-price-plans/</link><dc:creator>pg_1234</dc:creator><comments>https://news.ycombinator.com/item?id=39672021</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672021</guid></item><item><title><![CDATA[Tesla goes after Cybertruck owners selling their electric pickup trucks]]></title><description><![CDATA[
<p>Article URL: <a href="https://electrek.co/2024/03/11/tesla-goes-after-cybertruck-owners-selling-electric-pickup-trucks/">https://electrek.co/2024/03/11/tesla-goes-after-cybertruck-owners-selling-electric-pickup-trucks/</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672019">https://news.ycombinator.com/item?id=39672019</a></p>
<p>Points: 5</p>
<p># Comments: 1</p>
]]></description><pubDate>Mon, 11 Mar 2024 18:56:58 +0000</pubDate><link>https://electrek.co/2024/03/11/tesla-goes-after-cybertruck-owners-selling-electric-pickup-trucks/</link><dc:creator>mfiguiere</dc:creator><comments>https://news.ycombinator.com/item?id=39672019</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672019</guid></item><item><title><![CDATA[Apple has begun testing an AI-powered ad product]]></title><description><![CDATA[
<p>Article URL: <a href="https://www.businessinsider.com/apple-tests-ai-app-store-ads-performance-max-2024-3">https://www.businessinsider.com/apple-tests-ai-app-store-ads-performance-max-2024-3</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39672000">https://news.ycombinator.com/item?id=39672000</a></p>
<p>Points: 3</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 18:54:38 +0000</pubDate><link>https://www.businessinsider.com/apple-tests-ai-app-store-ads-performance-max-2024-3</link><dc:creator>mfiguiere</dc:creator><comments>https://news.ycombinator.com/item?id=39672000</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39672000</guid></item><item><title><![CDATA[Ask HN: Pull Requests for Databases]]></title><description><![CDATA[
<p>Hey HN,<p>I'm working on building a database management system tool and would love your insights and feedback on the plan. Here are some key features:<p>1. Pull Requests for Databases:
   - Users can submit pull requests for running queries in the production environment.
   - This feature enables running queries without direct access to the database.<p>2. Table Ownership:
   - Assign specific individuals as owners of different database tables.
   - Owners ensure thorough validation before queries are executed on their respective tables.<p>I'm excited about these features, but I'd greatly appreciate your thoughts and suggestions. Do you see any potential challenges or additional functionalities that could enhance this tool? Your feedback will be invaluable in shaping its development. Is this something that would improve your workflow? Thanks in advance!</p>
<hr>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39671990">https://news.ycombinator.com/item?id=39671990</a></p>
<p>Points: 1</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 18:54:01 +0000</pubDate><link>https://news.ycombinator.com/item?id=39671990</link><dc:creator>eric-ostholm</dc:creator><comments>https://news.ycombinator.com/item?id=39671990</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39671990</guid></item><item><title><![CDATA[Apple testing AI-powered ads platform]]></title><description><![CDATA[
<p>Article URL: <a href="https://9to5mac.com/2024/03/11/report-apple-testing-ai-powered-ads-platform/">https://9to5mac.com/2024/03/11/report-apple-testing-ai-powered-ads-platform/</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39671988">https://news.ycombinator.com/item?id=39671988</a></p>
<p>Points: 1</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 18:53:51 +0000</pubDate><link>https://9to5mac.com/2024/03/11/report-apple-testing-ai-powered-ads-platform/</link><dc:creator>cdme</dc:creator><comments>https://news.ycombinator.com/item?id=39671988</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39671988</guid></item><item><title><![CDATA[EU states agree to regulate Deliveroo, Uber workers' rights]]></title><description><![CDATA[
<p>Article URL: <a href="https://www.dw.com/en/eu-states-agree-to-regulate-deliveroo-uber-workers-rights/a-68495444">https://www.dw.com/en/eu-states-agree-to-regulate-deliveroo-uber-workers-rights/a-68495444</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39671985">https://news.ycombinator.com/item?id=39671985</a></p>
<p>Points: 1</p>
<p># Comments: 0</p>
]]></description><pubDate>Mon, 11 Mar 2024 18:53:44 +0000</pubDate><link>https://www.dw.com/en/eu-states-agree-to-regulate-deliveroo-uber-workers-rights/a-68495444</link><dc:creator>rntn</dc:creator><comments>https://news.ycombinator.com/item?id=39671985</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39671985</guid></item><item><title><![CDATA[The great American llama (and ostrich and emu) collapse]]></title><description><![CDATA[
<p>Article URL: <a href="https://www.washingtonpost.com/business/2024/03/07/llama-emu-ostrich-herds-down/">https://www.washingtonpost.com/business/2024/03/07/llama-emu-ostrich-herds-down/</a></p>
<p>Comments URL: <a href="https://news.ycombinator.com/item?id=39671983">https://news.ycombinator.com/item?id=39671983</a></p>
<p>Points: 2</p>
<p># Comments: 1</p>
]]></description><pubDate>Mon, 11 Mar 2024 18:53:39 +0000</pubDate><link>https://www.washingtonpost.com/business/2024/03/07/llama-emu-ostrich-herds-down/</link><dc:creator>bookofjoe</dc:creator><comments>https://news.ycombinator.com/item?id=39671983</comments><guid isPermaLink="false">https://news.ycombinator.com/item?id=39671983</guid></item></channel></rss>
"""
