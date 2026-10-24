# Giving on the website — today's plan

## What Lenco actually is

Lenco (lenco.co, "Lenco by Broadpay") is a business banking and payments
platform in Zambia. Their API is documented at **lenco-api.readme.io**.

**Details that matter, taken from their documentation:**

| | |
|---|---|
| Address | `https://api.lenco.co/access/v1` |
| Signing in | `Authorization: Bearer YOUR_TOKEN` |
| Getting a token | Email **support@lenco.co** |
| Replies | `{ "status": true/false, "message": "...", "data": { ... } }` |

## The one thing that is not what we hoped

Their API is built to **send money out** to people: bank transfers, bill
payments, POS terminals. There is **no endpoint for collecting money from a
customer**, and **no phone prompt**.

We read their complete list of endpoints. There is nothing that takes a
customer's phone number and sends them a payment prompt.

## How money comes IN to a business on Lenco

**Virtual accounts.** The church is given a real, unique account number that
belongs to it. A giver sends money to that number from their mobile money or
bank, and Lenco tells us the moment it lands.

From their documentation:

- `POST /virtual-accounts` creates one
- You can set the **exact amount** expected, and money in any other amount is
  automatically rejected
- You can add a **reference** so we know which giving it was
- A "dynamic" account expires after a short time, which is ideal for giving

So the honest version of the giving page is:

> The person enters their **name** and the **amount**. The site then gives them
> a **private account number for that amount**. They pay to it from mobile money
> or their bank, and we are told automatically when it arrives.

**No prompt on their phone.** That is the trade.

## Two ways forward

**A — Go with virtual accounts (recommended, works today)**
Uses only what we have read and verified. Nothing is guessed.
The giver types name and amount, is shown a private account number to pay, and
gets a clear confirmation when it lands.

**B — Ask Lenco whether they do prompts privately**
Some providers sell a collections or prompt product that is not in the public
documentation. If Lenco has one, it is exactly what you asked for.
Email support@lenco.co and ask. If they say yes, I will read that
documentation and wire it up properly.

**Both are worth doing:** ask them about B, and build A in the meantime.

## Today's plan

**Morning — done already**
- [x] Give page live with a real form
- [x] Zambian number checked before anything is sent
- [x] No card, no PIN, nothing stored
- [x] Abuse limit
- [x] Fails safely — never says a payment went through when it did not
- [x] Only the church's website may use it

**Next, once you have a Lenco token**
1. Email **support@lenco.co**, ask for an API token and ask about prompts
2. Paste the token into Cloudflare, named `LENCO_API_TOKEN` — never in chat
3. I rewrite the giving code against their real `POST /virtual-accounts`
4. The page shows a private account number and the amount to pay
5. We test with a small amount, your own phone, real money you control
6. Only then do we tell anyone else to use it

## What I need from you today

1. **Send that email** — I will give you the wording
2. **Paste the token** into Cloudflare when it arrives

## What I am not going to do

Write payment code against an endpoint that does not exist. If a person's
money went to the wrong place, or appeared to be taken when it was not, that is
far worse than the page saying "not yet".