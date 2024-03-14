# This file is placed in the Public Domain.
#
#
# pylint: disable=C,R,W1503


"no tests"


import unittest


from rssbot.modules.rss import Parser


class TestAtom(unittest.TestCase):

    def test_github(self):
        res = Parser.parse(TXT, "entry", "title,author,link")
        self.assertEqual(len(res), 20)


TXT = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/" xml:lang="en-US">
  <id>tag:github.com,2008:/xobjectz/objx/commits/master</id>
  <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commits/master"/>
  <link type="application/atom+xml" rel="self" href="https://github.com/xobjectz/objx/commits/master.atom"/>
  <title>Recent Commits to objx:master</title>
  <updated>2024-03-08T03:15:07Z</updated>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/935d09c548b9d00c9ddf5e1c542e3ae87a64ad58</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/935d09c548b9d00c9ddf5e1c542e3ae87a64ad58"/>
    <title>
        lintify
    </title>
    <updated>2024-03-08T03:15:07Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;lintify&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/4c462f9ec5366c0c2380cde178887ae737bcfbd5</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/4c462f9ec5366c0c2380cde178887ae737bcfbd5"/>
    <title>
        nits
    </title>
    <updated>2024-03-08T02:48:56Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;nits&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/4c02178656a44eb1376b9a75947c435bd7f7cade</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/4c02178656a44eb1376b9a75947c435bd7f7cade"/>
    <title>
        fix
    </title>
    <updated>2024-03-08T02:46:38Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;fix&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/726f8b7c1c3f66c8b94127015ea0c411d6eea3c7</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/726f8b7c1c3f66c8b94127015ea0c411d6eea3c7"/>
    <title>
        add tests
    </title>
    <updated>2024-03-08T02:38:25Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;add tests&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/bdcf5471184fcce61e7d393bf6e9ff9a140f8941</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/bdcf5471184fcce61e7d393bf6e9ff9a140f8941"/>
    <title>
        don&#39;t scan
    </title>
    <updated>2024-03-06T11:05:22Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;don&amp;#39;t scan&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/6ab6ad0461f4653aca3f838cd6fa22465198a4c6</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/6ab6ad0461f4653aca3f838cd6fa22465198a4c6"/>
    <title>
        add threads
    </title>
    <updated>2024-03-05T21:51:40Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;add threads&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/f326b3dc7476bca52f73f02c6984a8cad6a8dd4f</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/f326b3dc7476bca52f73f02c6984a8cad6a8dd4f"/>
    <title>
        crap scheduler
    </title>
    <updated>2024-03-05T21:47:57Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;crap scheduler&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/4e6b46dcae651ac954de368cc4ec54d1d646d7d3</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/4e6b46dcae651ac954de368cc4ec54d1d646d7d3"/>
    <title>
        add default
    </title>
    <updated>2024-03-05T21:18:07Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;add default&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/9c9e952e78addd03bb948509119dd9a05dd31309</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/9c9e952e78addd03bb948509119dd9a05dd31309"/>
    <title>
        okdan
    </title>
    <updated>2024-03-05T21:17:53Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;okdan&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/a154ba8b13adc835748528e67b24efdd9b9f2e84</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/a154ba8b13adc835748528e67b24efdd9b9f2e84"/>
    <title>
        fix tinder
    </title>
    <updated>2024-03-05T21:17:24Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;fix tinder&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/b701f4bfc7ead64da41f1c678170388761d2d4ba</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/b701f4bfc7ead64da41f1c678170388761d2d4ba"/>
    <title>
        use default decoder encoder
    </title>
    <updated>2024-03-05T15:31:34Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;use default decoder encoder&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/3015d910d2bfff0d0d6235eafce01a19a10fae6b</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/3015d910d2bfff0d0d6235eafce01a19a10fae6b"/>
    <title>
        fix tinder
    </title>
    <updated>2024-03-05T01:38:00Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;fix tinder&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/a10b73430ee5f92ce058a573fca6ce18d587cc1b</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/a10b73430ee5f92ce058a573fca6ce18d587cc1b"/>
    <title>
        back to threaded
    </title>
    <updated>2024-03-04T16:12:33Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;back to threaded&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/2ab24e8ee947eb7df1f4cd4b90599de4673f2188</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/2ab24e8ee947eb7df1f4cd4b90599de4673f2188"/>
    <title>
        ok
    </title>
    <updated>2024-03-04T13:19:49Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;ok&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/a082c2ecb4f2705a8210cfddb50864ab61e438c0</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/a082c2ecb4f2705a8210cfddb50864ab61e438c0"/>
    <title>
        fix tests
    </title>
    <updated>2024-03-04T12:18:25Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;fix tests&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/272e1e8cc994a68356b00080a541cd5d7067b166</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/272e1e8cc994a68356b00080a541cd5d7067b166"/>
    <title>
        add test
    </title>
    <updated>2024-03-04T12:18:13Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;add test&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/bf2755dc53c91dcc07c377ed87c93f694cf55e48</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/bf2755dc53c91dcc07c377ed87c93f694cf55e48"/>
    <title>
        remove tests
    </title>
    <updated>2024-03-02T15:06:11Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;remove tests&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/f79d778a851af4b531318932a946144d32679a33</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/f79d778a851af4b531318932a946144d32679a33"/>
    <title>
        up version
    </title>
    <updated>2024-03-02T15:05:30Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;up version&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/cf5d94f552fecc757056b3bdda7cfd09e98e4787</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/cf5d94f552fecc757056b3bdda7cfd09e98e4787"/>
    <title>
        up version
    </title>
    <updated>2024-03-02T15:05:09Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;up version&lt;/pre&gt;
    </content>
  </entry>
  <entry>
    <id>tag:github.com,2008:Grit::Commit/7843327257df86b6b48ff381ccbf7fc66b8bdcd1</id>
    <link type="text/html" rel="alternate" href="https://github.com/xobjectz/objx/commit/7843327257df86b6b48ff381ccbf7fc66b8bdcd1"/>
    <title>
        it&#39;s a library
    </title>
    <updated>2024-03-02T15:02:45Z</updated>
    <media:thumbnail height="30" width="30" url="https://avatars.githubusercontent.com/u/156056514?s=30&amp;v=4"/>
    <author>
      <name>xobjectz</name>
      <uri>https://github.com/xobjectz</uri>
    </author>
    <content type="html">
      &lt;pre style=&#39;white-space:pre-wrap;width:81ex&#39;&gt;it&amp;#39;s a library&lt;/pre&gt;
    </content>
  </entry>
</feed>
"""