curl -F grant_type=authorization_code \
-F client_id=u-s4t2ud-110e6a72c470ea3b61e2a1bc09acbd391dbb5fa23ecb37d0c8b88d513aa3865a \
-F client_secret=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 \
-F code=ed5a3d5d93355fd8a4533097b5a1fc9102659211f8bb1068c1d6f8654bf22935 \
-F redirect_uri="https://upgraded-dollop-q65pjww6654c67pp-8000.app.github.dev/auth42_callback" \
-X POST https://api.intra.42.fr/oauth/token
