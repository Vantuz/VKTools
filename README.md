# VKTools
A nifty set of some simple tools working with vk.com. Currently availaible: `vk_liker.py`

## vk_auth.py

Tool for acquiring VK API tokens

Requirements: `Python3`, `requests`, `mechanicalsoup`

Usage: run `./vk_auth.py login pass` (optionally with `--client_id CLIENT_ID --scope SCOPE`)

## vk_liker.py

Ultimate autoliker tool for vk.com

Requirements: `Python3`, `requests`

Usage:

1. Get access token with `wall` permission (more info [here](https://vk.com/dev/implicit_flow_user))
2. Put your access token in `tokenfile.json` file, following the sample here:
```json
{
	"default": "my",
	"tokens": {
		"my": "super_secret_token"
	}
}
```
3. Run `./vk_liker.py target_id [target_id ...]` (yeah, you can use multiple targets)
4. ?????
5. PROFIT!!1

Actually, this is a redesign of my old autoliker script (which i never show to anyone 'cause it is really poorly written)
inspired by [sandwwraith](https://github.com/sandwwraith/vk-liker-gun)
