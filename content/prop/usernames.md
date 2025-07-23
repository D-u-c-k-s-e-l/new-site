---
title: The Username Proposition
---

# The Username Proposition

Type: Proposition  
Pub: 2025-07-13 (but ideated before then)
Updated: 2025-07-22

## What's in a name?

Currently, there are a LOT of ways to represent usernames. Let's see just a few:

|            |                      |
| :--------- | :------------------- |
| most sites | `@username`          |
| reddit     | `r/username`         |
| fediverse  | `@username@place`    |
| matrix     | `@username:instance` |
| email      | `username@provider`  |

## Cleaning things up

Because there are so many ways, I thought I'd clean things up a bit.

## The system

To represent usernames, I propose we use =={platform}@{username}{@domain}==.

For example, john doe might have a matrix account ==!matrix@johndoe@example.com== or an email ==!email@johndoe@example.com==. These are equivalent to ==@johndoe:example.com== and ==johndoe@example.com==.

1. For platforms that don't require a URL, the ==@domain== is removed, for example ==twitter@johndoe==.
2. When referencing someone on the same server (for fedi, etc.), the ==@domain== may be removed as well.
3. The ==platform== may be omitted when referencing a user on the same platform. This means if you're on twitter and contacting John Doe (and also following rule 1), you just do ==@johndoe==.

## Additional rules

There are some characters you may add before a username to change how it displays. If you add these and the user would usually be pinged (sent a notification), they won't be.

- The `!` character escapes a username sequence, allowing you to show the raw text.
  this can be applied before any other one of these characters. For example, ==!!email@johndoe@example.com== will show ==!email@johndoe@example.com==.  
  This has been used repeatedly throughout this document to show examples without embedding links.
- The `~` character just disables pinging the user so you can be respectful of their attention.
- An `=` before a username will show the url only, and not the username. (i.e. ==!=reddit@user== will show ==https://www.reddit.com/u/user==)
- A `$` before a username will show the formatted username. (i.e. ==!$reddit@user== will show ==u/user==)

## Implementations

The main implementation of this proposition is on [my website](https://ducksel.xyz) which you are currently visiting. You can see this if I write ==!tumblr@helloiamduck==: tumblr@helloiamduck.

I also am working on an implementation of this for Jekyll, but I haven't published it yet.

Please [contact me](/contact/) if you would like help implementing this, have questions, or have already implemented it.

## Notes

Most platforms don't require adding their name before a username, so rule 3 is satisfied already.

Some platforms like [wafrn](https://wafrn.net) follow rule 2.

<br/><br/>

---

Freedom of usage:

I'm just putting this idea out there for fun. Do whatever you want with it forever for free :\)