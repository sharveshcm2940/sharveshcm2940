"""One-off: download Righteous + Space Mono and subset them to small .woff files in fonts/."""
import os, urllib.request
from fontTools import subset

BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
FONTS = {
    "display.woff": "righteous/Righteous-Regular.ttf",
    "mono-400.woff": "spacemono/SpaceMono-Regular.ttf",
    "mono-700.woff": "spacemono/SpaceMono-Bold.ttf",
}
UNICODES = list(range(0x20, 0x7F)) + [0xB7, 0x2190, 0x2191, 0x2192, 0x2193, 0x2605]
os.makedirs("fonts", exist_ok=True)
for out, path in FONTS.items():
    ttf = "fonts/_tmp.ttf"
    urllib.request.urlretrieve(BASE + path, ttf)
    opts = subset.Options(); opts.flavor = "woff"; opts.layout_features = ["kern"]
    font = subset.load_font(ttf, opts)
    sub = subset.Subsetter(opts); sub.populate(unicodes=UNICODES); sub.subset(font)
    subset.save_font(font, "fonts/" + out, opts)
    print(out, os.path.getsize("fonts/" + out), "bytes")
os.remove("fonts/_tmp.ttf")
