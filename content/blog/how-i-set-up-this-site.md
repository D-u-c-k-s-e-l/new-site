---
title: How I Set Up This Site
published: 2025-05-24
---

# How I Set Up This Site

Blog article  
2025-05-24

## Info

I thought that I'd write a small blog thing (are they posts, articles, idk...) about how I set this site up. It was a fun challenge, and I thought it would be good to share.

To start me down this path, I had already built a decent site with github's github.io system, but it wasn't really giving me all that I wanted, and the codebase was a bit of a mess. A github.io site feels like github owns, it rather than you.

To solve the problem of not having my own site, I needed to first solve the easier problem: a domain.

## A domain

To start out, I was thinking about what I should get for a domain. I'd heard of these unicode domains where you can put emojis and whatnot in the url. Unfortunately, after some research, I learned that the only people who will sell you those are random countries. (It's a security thing.) With my head down, I turned away from [duck emoji].dev, and started being realistic.

My next options were all ducksel.something. Ducksel has been my name online for quite a while, and I thought I might as well name my personal site after myself.

<!-- cspell: words godaddy -->
Once I had settled on this and done some digging, I found the cheapest place to buy domains: gen.xyz. Sure, .xyz looks childish and it's not a *real* domain provider like godaddy, but it worked great, and with only $10, I bought a domain for a year!

Domain in hand, I now had a new problem: hosting

## Hosting

<!-- cspell: words neocities -->
Now where does one put a website, I wondered. I had many options. I could self-host, exposing my PII, and breaking the contract with my ISP. I could pay a cloud provider an atrocious amount of money. Or, I could go on some weird site that does very specific types of website like neocities or wordpress. For a while I was going to be paying $5/mo for someone to host my flask server, when I stumbled onto NearlyFreeSpeech.

NearlyFreeSpeech offers hosting for a minimum price of ~$3.65/yr. That was so exciting that I abandoned any other searches and dove in head first. I signed up, created a site, put my domain with their servers, and installed some flask stuff. What came next was predictable.

<!-- cspell: words venv -->
NFS, you see, is a very DIY sort of server provider, and if you go over their limits, they do charge. I had set up a Flask+Waitress server on their cheapest tier, and even the storage from the python .venv was costing me extra. Flask, too, is not a lightweight process, and the memory and CPU was *also* costing me a bit extra. I shut the site down, and went to ponder alternatives.

After the Flask failure, I remembered what NFS had said in various places across their website; static sites are cheaper. Armed with that knowledge, but not knowing a thing about apache, I turned off their apache daemon and tried installing nginx.

It turns out that it is very hard to compile nginx from scratch, and my friend and I, after an hour or two of trying, decided that it wasn't worth it. I was back to square zero.

Now that I had failed in both Flask and nginx, I took a break, then conceded to apache's tyranny. I told NFS to put apache back, and decided to live with it.

## Synchronization

At this point, it had been a month or two of having my hosting and domain. I had, by now, realized that

1. this is a static site that I'm gonna be writing and
2. whatever changes I make to the site need to be pulled through github, and onto the server

I started by writing a python script to compile the site. I reasoned (correctly) that I'm going to want my own very simple templating engine, with really good markdown support, and I'm going to have fun making it. I also reasoned (incorrectly) that it would make sense to hold the content on one branch, and the compiled site on another branch.

After a week('s worth) of work, I realized that I was incorrect, and that it should just use git's sparse feature.

### Git's Sparse Feature

So, thanks to Torvalds, it turns out that there's a really convenient way to deal with the fact that sometimes you only need one directory. After deeply reading the git docs, I found this out. I don't have my sync script up on github yet, but if I put it there, I'll link it here.

Anyway, you can pull down exclusively the `output/` folder (for example) of a repo by running,

```bash
git init
# <-- you would `remote add origin` on this line
git config core.sparseCheckout true
```

Then putting the line `output/` in the repo's `.git/info/sparse-checkout`, then doing your git pull.

Why is this a thing? I don't know. Is it kinda cool? Yeah!

So I used this thing I'd found in a script on my NFS private directory, while also telling it to store no history. What a free deal!

I did use a bit of AI to help write the script, but mostly because it's better about not hardcoding everything. Now, every hour, whatever is on the github repo is pulled up onto the server!

## Content

### Marking Down

Jumping back to before I discovered the cool git thing, I had begun working on my site.  I was thinking of all the things I had loved and hated about markdown over the years. I realized a few things.

1. I like having the ability to put $\LaTeX$ into things
2. That ==highlighted text== thing some note apps do is kinda cool
3. I need syntax highlighting
4. When I use markdown, I miss the %1c%%%2o%%%3l%%%4o%%%5r%%%6s%% you can use in a terminal
5. It should be easy to link to people's social media accounts
6. Nerd fonts

To solve #1, I just used MathJax. No use reinventing the wheel. The same with #6; just use Nerd Fonts if you want them.

For #3, I used codehilite, because it just made sense if I'm already using python markdown.

As for #2 #4 and #5, I got myself custom markdown extensions! Yes, AI helped a little, but overall, it's all my ideas, and mostly my code.

### Marking Up

Meanwhile, I also needed a template to house my ideas. I decided make it by hand with HTML. The final design looks amazing, imo, and even looks good in Lynx. (nothing looks good in Lynx)

I wanted the site to look and feel unique, so I pulled out a color picker, and picked out 18 or so colors by hand, to set the vibe. I later had to adjust the foreground color to fix some contrast issues, but that's what you get for hand-picking colors. I decided that I might as well write a blog article every so often, so I made a blog link.

It turns out that the less you style a website, the more responsive it becomes (aside from mobile experience). This was to my advantage, as I wanted to make my website look good anywhere. (yes, even Lynx). Somehow, the little worms at top and bottom of the content made it in there. I don't know why or how, but I'm not mean enough to kick them out, so they're staying.

Apparently, you "should" have a robots.txt file. I'm not sure what goes in there, so I just said "block all robots". Will this wreck my SEO? Absolutely! Do I care? No. Should I really not do that? Probably, but I honestly don't feel like researching it more. All I know is this will block some kind scrapers from stealing from me, and that seems like an okay thing.

### htaccess

Something I learned on this journey was that apache has magic files called `.htaccess`. How do they work? Magic, I said.

Apparently, to make the URL not have that ugly ".html" on it, you need to tell the htaccess file to pretend that the .html is there. Why? I don't know.

Anyway, I added one of these.

## What I Got

> *I've got rhythm*  
> *I've got music*  
> *I've got my gal*  
> *Who could ask for anything more?*  
> -- "I've got Rhythm", Crazy for You

After this journey, I ended up with a pretty cool website that you're currently browsing. This website (aside from the nerd font icons, sorry Lynx) should work perfectly in any and all browsers, and that makes me pretty happy. I learned about creating and hosting websites, compilers, regex, markdown, and a CSS trick to make the footer snap to the bottom.

I have not been sponsored by anybody mentioned here, this is all my opinion and my money.
