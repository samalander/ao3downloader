import argparse
import ao3downloader.strings as strings
from ao3downloader.actions.ao3download import action as ao3_download_action
from ao3downloader.actions.getlinks import action as links_only_action
from ao3downloader.actions.enterlinks import action as file_input_action
from ao3downloader.actions.updatefics import action as update_epubs_action
from ao3downloader.actions.updateseries import action as update_series_action
from ao3downloader.actions.redownload import action as re_download_action
from ao3downloader.actions.markedforlater import action as marked_for_later_action
from ao3downloader.actions.pinboarddownload import action as pinboard_download_action
from ao3downloader.actions.logvisualization import action as log_visualization_action
from ao3downloader.actions.ignorelist import action as ignorelist_action

# Base parser and global arguments
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--login", action="store_true")
parser.add_argument("-u", "--username")
parser.add_argument("-p", "--password")
parser.add_argument("--save-password", action="store_true")
parser.add_argument("--download-types")
parser.add_argument("--save-download-types", action="store_true")
parser.add_argument("--use-saved-download-types", action="store_true")
parser.add_argument("--all-works-in-series", action="store_true")
parser.add_argument("--stop-page-number", type=int, default=1)
parser.add_argument("--download-images", action="store_true")

# Subparsers
subparsers = parser.add_subparsers(title=strings.ARGS_COMMANDS, dest="command")

# menu subparser (default)
menu = subparsers.add_parser("menu", help=strings.ACTION_DESCRIPTION_DISPLAY_MENU+' ({})'.format(strings.ARGS_DEFAULT), description=strings.ACTION_DESCRIPTION_DISPLAY_MENU)
subparsers.default = "menu"

# download subparser
download = subparsers.add_parser("download", aliases=["d"], help=strings.ACTION_DESCRIPTION_AO3, description=strings.ACTION_DESCRIPTION_AO3)
download.set_defaults(func=ao3_download_action)
download.add_argument("--url")

# links subparser
links = subparsers.add_parser("links", aliases=["l"], help=strings.ACTION_DESCRIPTION_LINKS_ONLY, description=strings.ACTION_DESCRIPTION_LINKS_ONLY)
links.set_defaults(func=links_only_action)

# file subparser
file = subparsers.add_parser("file", aliases=["f"], help=strings.ACTION_DESCRIPTION_FILE_INPUT, description=strings.ACTION_DESCRIPTION_FILE_INPUT)
file.set_defaults(func=file_input_action)

# update subparser
update = subparsers.add_parser("update", aliases=["u"], help=strings.ACTION_DESCRIPTION_UPDATE, description=strings.ACTION_DESCRIPTION_UPDATE)
update.set_defaults(func=update_epubs_action)

# series subparser
series = subparsers.add_parser("series", aliases=["s"], help=strings.ACTION_DESCRIPTION_UPDATE_SERIES, description=strings.ACTION_DESCRIPTION_UPDATE_SERIES)
series.set_defaults(func=update_series_action)

# re-download subparser
re_download = subparsers.add_parser("re-download", aliases=["r"], help=strings.ACTION_DESCRIPTION_REDOWNLOAD, description=strings.ACTION_DESCRIPTION_REDOWNLOAD)
re_download.set_defaults(func=re_download_action)

# marked subparser
marked = subparsers.add_parser("marked", aliases=["m"], help=strings.ACTION_DESCRIPTION_MARKED_FOR_LATER, description=strings.ACTION_DESCRIPTION_MARKED_FOR_LATER)
marked.set_defaults(func=marked_for_later_action)

# pinboard subparser
pinboard = subparsers.add_parser("pinboard", aliases=["p"], help=strings.ACTION_DESCRIPTION_PINBOARD, description=strings.ACTION_DESCRIPTION_PINBOARD)
pinboard.set_defaults(func=pinboard_download_action)

# log subparser
log = subparsers.add_parser("log", aliases=["v"], help=strings.ACTION_DESCRIPTION_VISUALIZATION, description=strings.ACTION_DESCRIPTION_VISUALIZATION)
log.set_defaults(func=log_visualization_action)

# ignore subparser
ignore = subparsers.add_parser("ignore", aliases=["i"], help=strings.ACTION_DESCRIPTION_CONFIGURE_IGNORELIST, description=strings.ACTION_DESCRIPTION_CONFIGURE_IGNORELIST)
ignore.set_defaults(func=ignorelist_action)

# Parse provided arguments, if any
args = parser.parse_args()

def command_is(cmd):
    return args.command == cmd

def has_args():
	return not command_is("menu")

def action():
    try:
        args.func()
    except Exception as e:
        print(str(e))

def has_arg(arg_name):
    try:
        arg = getattr(args, arg_name)
    except Exception as e:
        return False
    return arg is not None

def get_arg(arg_name):
    if not has_arg(arg_name):
        return
    return getattr(args, arg_name)

def arg_or_input(arg_name):
    arg=get_arg(arg_name)
    if arg:
        return arg
    else:
        return input()

def arg_yn_or_input(arg_name):
    arg=get_arg(arg_name)
    if arg == True:
        return strings.PROMPT_YES
    elif has_args():
        return strings.PROMPT_NO
    else:
        return input()