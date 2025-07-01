import argparse
import json
import requests
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import sys
import os
from fake_useragent import UserAgent
from colorama import Fore, Style, init

init(autoreset=True)

class Sn0wPlus:
    def __init__(self):
        self.ua = UserAgent()
        self.sites = self._load_sites()
        self.found = []
        self.lock = threading.Lock()
        self.animation_chars = "⢿⣻⣽⣾⣷⣯⣟⡿"
        self.animation_running = False

    def _load_sites(self):
        return {
            "twitter": "https://twitter.com/{}",
            "github": "https://github.com/{}",
            "reddit": "https://www.reddit.com/user/{}",
            "instagram": "https://www.instagram.com/{}",
            "facebook": "https://www.facebook.com/{}",
            "youtube": "https://www.youtube.com/{}",
            "linkedin": "https://www.linkedin.com/in/{}",
            "pinterest": "https://www.pinterest.com/{}",
            "tumblr": "https://{}.tumblr.com",
            "flickr": "https://www.flickr.com/people/{}",
            "vimeo": "https://vimeo.com/{}",
            "soundcloud": "https://soundcloud.com/{}",
            "spotify": "https://open.spotify.com/user/{}",
            "medium": "https://medium.com/@{}",
            "devto": "https://dev.to/{}",
            "tiktok": "https://www.tiktok.com/@{}",
            "twitch": "https://www.twitch.tv/{}",
            "steam": "https://steamcommunity.com/id/{}",
            "gitlab": "https://gitlab.com/{}",
            "bitbucket": "https://bitbucket.org/{}/",
            "keybase": "https://keybase.io/{}",
            "hackerone": "https://hackerone.com/{}",
            "bugcrowd": "https://bugcrowd.com/{}",
            "codepen": "https://codepen.io/{}",
            "behance": "https://www.behance.net/{}",
            "dribbble": "https://dribbble.com/{}",
            "foursquare": "https://foursquare.com/{}",
            "gravatar": "https://en.gravatar.com/{}",
            "slideshare": "https://www.slideshare.net/{}",
            "lastfm": "https://www.last.fm/user/{}",
            "goodreads": "https://www.goodreads.com/{}",
            "imgur": "https://imgur.com/user/{}",
            "patreon": "https://www.patreon.com/{}",
            "wikipedia": "https://en.wikipedia.org/wiki/User:{}",
            "500px": "https://500px.com/{}",
            "deviantart": "https://{}.deviantart.com",
            "etsy": "https://www.etsy.com/shop/{}",
            "roblox": "https://www.roblox.com/user.aspx?username={}",
            "scribd": "https://www.scribd.com/{}",
            "bandcamp": "https://www.bandcamp.com/{}",
            "kaggle": "https://www.kaggle.com/{}",
            "instructables": "https://www.instructables.com/member/{}",
            "hubpages": "https://hubpages.com/@{}",
            "wattpad": "https://www.wattpad.com/user/{}",
            "canva": "https://www.canva.com/{}",
            "reverbnation": "https://www.reverbnation.com/{}",
            "trakt": "https://www.trakt.tv/users/{}",
            "venmo": "https://venmo.com/{}",
            "cashapp": "https://cash.app/${}",
            "paypal": "https://www.paypal.me/{}",
            "gumroad": "https://gumroad.com/{}",
            "unsplash": "https://unsplash.com/@{}",
            "pypi": "https://pypi.org/user/{}",
            "npm": "https://www.npmjs.com/~{}",
            "dockerhub": "https://hub.docker.com/u/{}",
            "quora": "https://www.quora.com/profile/{}",
            "9gag": "https://www.9gag.com/u/{}",
            "ifttt": "https://ifttt.com/p/{}",
            "sourceforge": "https://sourceforge.net/u/{}",
            "archive": "https://archive.org/details/@{}",
            "disqus": "https://disqus.com/{}",
            "ello": "https://ello.co/{}",
            "mixcloud": "https://www.mixcloud.com/{}/",
            "producthunt": "https://www.producthunt.com/@{}",
            "tinder": "https://www.tinder.com/@{}",
            "okcupid": "https://www.okcupid.com/profile/{}",
            "badoo": "https://badoo.com/profile/{}",
            "meetup": "https://www.meetup.com/members/{}",
            "vk": "https://vk.com/{}",
            "telegram": "https://t.me/{}",
            "weibo": "https://www.weibo.com/{}",
            "douban": "https://www.douban.com/people/{}",
            "qq": "https://user.qzone.qq.com/{}",
            "baidu": "https://tieba.baidu.com/home/main?un={}",
            "zhihu": "https://www.zhihu.com/people/{}",
            "xiaohongshu": "https://www.xiaohongshu.com/user/profile/{}",
            "line": "https://line.me/ti/p/{}",
            "kakao": "https://story.kakao.com/{}",
            "naver": "https://blog.naver.com/{}",
            "pixiv": "https://www.pixiv.net/users/{}",
            "nicovideo": "https://www.nicovideo.jp/user/{}",
            "hatena": "https://profile.hatena.ne.jp/{}/",
            "fc2": "https://blog.fc2.com/{}/",
            "ameblo": "https://ameblo.jp/{}",
            "wix": "https://{}.wixsite.com/website",
            "blogger": "https://{}.blogspot.com",
            "wordpress": "https://{}.wordpress.com",
            "tistory": "https://{}.tistory.com",
            "weebly": "https://{}.weebly.com",
            "yandex": "https://yandex.ru/q/loves/{}",
            "livejournal": "https://{}.livejournal.com",
            "skyrock": "https://{}.skyrock.com",
            "jimdo": "https://{}.jimdosite.com",
            "webnode": "https://{}.webnode.com",
            "overblog": "https://{}.over-blog.com",
            "blogfa": "https://{}.blogfa.com",
            "blogspot": "https://{}.blogspot.com",
            "typepad": "https://{}.typepad.com",
            "hubzilla": "https://{}.hubzilla.org",
            "diaspora": "https://{}.diaspora.org",
            "gnusocial": "https://{}.gnusocial.net",
            "mastodon": "https://{}.mastodon.social",
            "pleroma": "https://{}.pleroma.social",
            "misskey": "https://{}.misskey.io",
            "writefreely": "https://{}.writefreely.org",
            "microblog": "https://{}.micro.blog",
            "writeas": "https://{}.write.as",
            "medium": "https://medium.com/@{}",
            "substack": "https://{}.substack.com",
            "ghost": "https://{}.ghost.io",
            "blot": "https://{}.blot.im",
            "bearblog": "https://{}.bearblog.dev",
            "neocities": "https://{}.neocities.org",
            "codidact": "https://{}.codidact.com",
            "discourse": "https://{}.discourse.group",
            "flarum": "https://{}.flarum.cloud",
            "phpbb": "https://{}.phpbb.com",
            "mybb": "https://{}.mybb.com",
            "smf": "https://{}.smf.com",
            "vanilla": "https://{}.vanillaforums.com",
            "xenforo": "https://{}.xenforo.com",
            "invision": "https://{}.invisioncommunity.com",
            "nodebb": "https://{}.nodebb.org",
            "discord": "https://discord.com/users/{}",
            "slack": "https://{}.slack.com",
            "matrix": "https://matrix.to/#/@{}:matrix.org",
            "irc": "https://webchat.freenode.net/#{}",
            "signal": "https://signal.me/#{}",
            "whatsapp": "https://wa.me/{}",
            "viber": "https://viber.com/{}",
            "line": "https://line.me/ti/p/{}",
            "wechat": "https://web.wechat.com/{}",
            "kik": "https://kik.me/{}",
            "skype": "https://web.skype.com/{}",
            "zoom": "https://zoom.us/{}",
            "teams": "https://teams.microsoft.com/{}",
            "hangouts": "https://hangouts.google.com/{}",
            "telegram": "https://t.me/{}",
            "threema": "https://threema.id/{}",
            "session": "https://getsession.org/{}",
            "status": "https://join.status.im/{}",
            "briar": "https://briarproject.org/{}",
            "tox": "https://tox.chat/{}",
            "jami": "https://jami.net/{}",
            "wire": "https://wire.com/{}",
            "element": "https://element.io/{}",
            "riot": "https://riot.im/{}",
            "mattermost": "https://mattermost.com/{}",
            "rocketchat": "https://rocket.chat/{}",
            "zulip": "https://zulip.com/{}",
            "jitsi": "https://jitsi.org/{}",
            "bigbluebutton": "https://bigbluebutton.org/{}",
            "whereby": "https://whereby.com/{}",
            "appearin": "https://appear.in/{}",
            "gotomeeting": "https://gotomeeting.com/{}",
            "joinme": "https://join.me/{}",
            "teamviewer": "https://teamviewer.com/{}",
            "anydesk": "https://anydesk.com/{}",
            "ultravnc": "https://ultravnc.com/{}",
            "tightvnc": "https://tightvnc.com/{}",
            "realvnc": "https://realvnc.com/{}",
            "logmein": "https://logmein.com/{}",
            "chrome": "https://remotedesktop.google.com/{}",
            "microsoft": "https://remote.desktop.microsoft.com/{}",
            "apple": "https://remotedesktop.apple.com/{}",
            "amazon": "https://workspaces.amazon.com/{}",
            "citrix": "https://citrix.com/{}",
            "vmware": "https://vmware.com/{}",
            "parallels": "https://parallels.com/{}",
            "virtualbox": "https://virtualbox.org/{}",
            "qemu": "https://qemu.org/{}",
            "docker": "https://docker.com/{}",
            "kubernetes": "https://kubernetes.io/{}",
            "openshift": "https://openshift.com/{}",
            "rancher": "https://rancher.com/{}",
            "mesos": "https://mesos.apache.org/{}",
            "nomad": "https://nomadproject.io/{}",
            "consul": "https://consul.io/{}",
            "vault": "https://vaultproject.io/{}",
            "terraform": "https://terraform.io/{}",
            "packer": "https://packer.io/{}",
            "vagrant": "https://vagrantup.com/{}",
            "ansible": "https://ansible.com/{}",
            "puppet": "https://puppet.com/{}",
            "chef": "https://chef.io/{}",
            "salt": "https://saltstack.com/{}",
            "cfengine": "https://cfengine.com/{}",
            "juju": "https://juju.is/{}",
            "cloudify": "https://cloudify.co/{}",
            "openstack": "https://openstack.org/{}",
            "opennebula": "https://opennebula.org/{}",
            "proxmox": "https://proxmox.com/{}",
            "xenserver": "https://xenserver.org/{}",
            "kvm": "https://www.linux-kvm.org/{}",
            "xen": "https://xenproject.org/{}",
            "hyperv": "https://microsoft.com/hyperv/{}",
            "vmware": "https://vmware.com/{}",
            "virtualbox": "https://virtualbox.org/{}",
            "parallels": "https://parallels.com/{}",
            "qemu": "https://qemu.org/{}",
            "bochs": "https://bochs.sourceforge.io/{}",
            "dosbox": "https://dosbox.com/{}",
            "wine": "https://winehq.org/{}",
            "reactos": "https://reactos.org/{}",
            "haiku": "https://haiku-os.org/{}",
            "freedos": "https://freedos.org/{}",
            "kolibrios": "https://kolibrios.org/{}",
            "menuets": "https://menuetos.net/{}",
            "templeos": "https://templeos.org/{}",
            "serenity": "https://serenityos.org/{}",
            "reactos": "https://reactos.org/{}",
            "haiku": "https://haiku-os.org/{}",
            "freedos": "https://freedos.org/{}",
            "kolibrios": "https://kolibrios.org/{}",
            "menuets": "https://menuetos.net/{}",
            "templeos": "https://templeos.org/{}",
            "serenity": "https://serenityos.org/{}",
            "reactos": "https://reactos.org/{}",
            "haiku": "https://haiku-os.org/{}",
            "freedos": "https://freedos.org/{}",
            "kolibrios": "https://kolibrios.org/{}",
            "menuets": "https://menuetos.net/{}",
            "templeos": "https://templeos.org/{}",
            "serenity": "https://serenityos.org/{}",
            "reactos": "https://reactos.org/{}",
            "haiku": "https://haiku-os.org/{}",
            "freedos": "https://freedos.org/{}",
            "kolibrios": "https://kolibrios.org/{}",
            "menuets": "https://menuetos.net/{}",
            "templeos": "https://templeos.org/{}",
            "serenity": "https://serenityos.org/{}",
            "reactos": "https://reactos.org/{}",
            "haiku": "https://haiku-os.org/{}",
            "freedos": "https://freedos.org/{}",
            "kolibrios": "https://kolibrios.org/{}",
            "menuets": "https://menuetos.net/{}",
            "templeos": "https://templeos.org/{}",
            "serenity": "https://serenityos.org/{}",
            "reactos": "https://reactos.org/{}",
            "haiku": "https://haiku-os.org/{}",
            "freedos": "https://freedos.org/{}",
            "kolibrios": "https://kolibrios.org/{}",
            "menuets": "https://menuetos.net/{}",
            "templeos": "https://templeos.org/{}",
            "serenity": "https://serenityos.org/{}",
        }

    def _animate(self):
        while self.animation_running:
            for c in self.animation_chars:
                sys.stdout.write(f"\r{Fore.CYAN}Scanning {c}{Style.RESET_ALL}")
                sys.stdout.flush()
                time.sleep(0.1)

    def _check_site(self, site, username):
        url = self.sites[site]
        try:
            headers = {"User-Agent": self.ua.random}
            r = requests.get(url.format(username), headers=headers, timeout=10)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                title = soup.title.string.lower() if soup.title else ""
                if "404" not in title and "not found" not in title:
                    with self.lock:
                        self.found.append((site, url.format(username)))
        except:
            pass

    def scan(self, username, sites=None):
        self.found = []
        selected_sites = self.sites if not sites else {k: v for k, v in self.sites.items() if k in sites}
        
        self.animation_running = True
        t = threading.Thread(target=self._animate)
        t.daemon = True
        t.start()

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(self._check_site, site, username) for site in selected_sites]
            for future in futures:
                future.result()

        self.animation_running = False
        time.sleep(0.5)
        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.flush()

        return self.found

def print_banner():
    print(f"""
    {Fore.CYAN}
     _____ _  _______      ____   ____
    / ___/| |/ / ___/     / __ \\ / __ \\
    \\__ \\ |   /\\__ \\     / / / // / / /
   ___/ / /   |___/ /    / /_/ // /_/ / 
  /____/_/|_/____/_____/\\____/ \\____/  
                 /_____/ {Fore.MAGENTA}v1.0 Coder/autor/OWNER->@rootkitov{Fore.CYAN}
    {Style.RESET_ALL}
    """)

def main():
    parser = argparse.ArgumentParser(description=f"{Fore.CYAN}Sn0w++ — Ultra OSINT Radar{Style.RESET_ALL}")
    parser.add_argument("query", help="Username, email, or name")
    parser.add_argument("--site", nargs="+", help="Specific sites to check")
    args = parser.parse_args()

    print_banner()

    sn0w = Sn0wPlus()
    results = sn0w.scan(args.query, args.site)

    if results:
        print(f"\n{Fore.GREEN}[+] Found ({len(results)}):{Style.RESET_ALL}")
        for site, url in results:
            print(f"{Fore.YELLOW}🔗 {site}:{Style.RESET_ALL} {url}")
    else:
        print(f"\n{Fore.RED}[-] No results found.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()