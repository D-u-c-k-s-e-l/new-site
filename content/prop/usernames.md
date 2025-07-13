---
title: The Username Proposition
---

# The Username Proposition

Type: Proposition  
Pub: 2025-07-13 (but ideated before then)

## What's in a name?

Currently, there are a LOT of ways to represent usernames. Let's see just a few:

- `@ username : instance` (matrix)
- `@ username @ place` (fedi)
- `@ username` (most sites)
- `r/username` (reddit)
- `username @ provider` (email)

## Cleaning things up

Because there are so many ways, I thought I'd clean things up a bit.

## The system

To represent usernames, I propose we use =={platform} @ {username} {@ location}==.

For example, john doe might have a matrix account ==matrix @ johndoe @ example.com== or an email ==email @ johndoe @ example.com==. These are equivalent to ==@johndoe:example.com== and ==johndoe @ example.com==.

1. For platforms that don't require a URL, the ==@ location== is removed, for example ==twitter @ johndoe==.
2. When referencing someone on the same server (for fedi, etc.), the ==@ location== may be removed as well.
3. The ==platform== may be omitted when referencing a user on the same platform. This means if you're on twitter and contacting John Doe (and also following rule 1), you just do ==@johndoe==.

## Implementations

The only current implementation of this system (as I'm aware) is on [my website](https://ducksel.xyz). This is why I have added the extra spaces and highlights in explaining this. A real email for john doe would be email@johndoe@example.com

Most platforms don't require adding their name before a username, so rule 3 is satisfied already.

Some platforms like [wafrn](https://wafrn.net) follow rule 2.

---

I'm just putting this idea out there for fun. Do whatever you want with it forever for free :\)