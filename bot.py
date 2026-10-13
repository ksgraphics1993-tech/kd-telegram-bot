import asyncio
import logging
import sqlite3
from telethon import TelegramClient, events
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Logging setup
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)

# Credentials
API_ID = 35029821
API_HASH = "756fb3767624b5a134ee947cf7c0d756"

# Sources
SOURCES = [
    -1003767231046,  # Source 1 (Bot 1 to 4)
    -1004416415348,  # Source 2 (Bot 5 to 8)
    -1004479610291,  # Source 3 (Bot 9 to 10)
]

DB_NAME = "queue_kd_1.db"

# Footer Text
FOOTER_TEXT = """〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️
📢 Official Backup & Kanda Hub
👉https://t.me/Official_Backup_Kanda_Hub
✦ HOW TO WATCH • VIDEO TUTORIALS ✦
👉https://t.me/how_to_watch_videos_tutorial
〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️
💎 Lɪɴᴋ ᴘᴀʀ ᴄʟɪᴄᴋ ᴋᴀʀᴋᴇ ᴘʟᴀʏᴇʀ ɪɴsᴛᴀʟʟ ᴋᴀʀᴇ , ᴠɪᴅᴇᴏ ᴜsᴍᴇ ʜɪ ᴘʟᴀʏ ʜOGI ✅"""


def init_db():
  conn = sqlite3.connect(DB_NAME)
  c = conn.cursor()
  c.execute("""
        CREATE TABLE IF NOT EXISTS message_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            msg_id INTEGER,
            source_chat INTEGER,
            UNIQUE(msg_id, source_chat)
        )
    """)
  conn.commit()
  conn.close()


# Bot Configurations
BOTS_DATA = [
    {
        "name": "Bot_1",
        "token": "8915225036:AAGz4CPXN2fEkW98-NxQnV2xF86tvB09-w8",
        "source_idx": 0,
        "destinations": [
            -1003911116307,
            -1003918864512,
            -1003886334500,
            -1003908437367,
            -1003874348126,
            -1003876437719,
            -1003847385528,
            -1003875919536,
            -1003990465683,
            -1003900691697,
            -1003901812118,
            -1003843074222,
            -1003904380112,
            -1003945027668,
            -1003825382974,
            -1003828739132,
            -1003780468257,
            -1003845370855,
            -1003758874929,
            -1003766830845,
            -1003435863498,
            -1003749395663,
            -1003366835605,
            -1003708535049,
            -1003839786735,
            -1003944087778,
            -1003945438020,
            -1003998601614,
            -1003930405035,
        ],
    },
    {
        "name": "Bot_2",
        "token": "8927936850:AAEbxhXfE14C0j6IFWZxhXR9RCfv8mrmB9E",
        "source_idx": 0,
        "destinations": [
            -1003749543552,
            -1003725197771,
            -1003865954557,
            -1003865229194,
            -1003841286977,
            -1003839693977,
            -1003829397367,
            -1003759878283,
            -1003763859494,
            -1003766445873,
            -1003772747831,
            -1003555988592,
            -1003821342685,
            -1003814933340,
            -1003799936393,
            -1003796079444,
            -1003777488259,
            -1003927883382,
            -1003931017577,
            -1003926407278,
            -1003911964256,
            -1003910751171,
            -1003902835773,
            -1003881112731,
            -1003879395088,
            -1003758062779,
            -1003726662324,
            -1003752418465,
            -1003751172009,
        ],
    },
    {
        "name": "Bot_3",
        "token": "8875604127:AAGp_rIvq3XwOtGA8XheOANySzDbRRXoHlE",
        "source_idx": 0,
        "destinations": [
            -1002975167546,
            -1002955294227,
            -1002657733796,
            -1003924257350,
            -1003722649284,
            -1003722139007,
            -1003709055222,
            -1003003450232,
            -1003009149881,
            -1003231741270,
            -1003335469700,
            -1003385239002,
            -1003442782382,
            -1003552972289,
            -1003491789754,
            -1003907167414,
            -1003913001793,
            -1003914088968,
            -1003915646793,
            -1003917726337,
            -1003916076721,
            -1003920783995,
            -1003920916269,
            -1003686121461,
            -1003664598121,
            -1003636009600,
            -1003617560582,
            -1003573895955,
            -1003562467880,
        ],
    },
    {
        "name": "Bot_4",
        "token": "8862059865:AAGs4r5ePN0st9LlALBp92JJjYV_KzPAePA",
        "source_idx": 0,
        "destinations": [
            -1004336993231,
            -1004367728460,
            -1004462530205,
            -1003987038402,
            -1003990016609,
            -1003990958817,
            -1003994400247,
            -1003998105741,
            -1003998204195,
            -1003921321781,
            -1003920928228,
            -1003934472230,
            -1003972851596,
            -1003976317057,
            -1003979007636,
            -1003980159467,
            -1003985509716,
            -1003984220036,
            -1003985481197,
            -1003970345184,
            -1003970271109,
            -1003960501820,
            -1003969243802,
            -1003960273974,
            -1003958012407,
            -1003957867871,
            -1003949790398,
            -1003943586285,
            -1003939596161,
            -1003939343227,
        ],
    },
    {
        "name": "Bot_5",
        "token": "8887260713:AAFTbu2XXGEpYbW1KKHB753WPwf0Rr3hfdU",
        "source_idx": 1,
        "destinations": [
            -1004262706797,
            -1004292834191,
            -1004294286103,
            -1004295906913,
            -1004295957735,
            -1004311032162,
            -1004299927349,
            -1004360386250,
            -1004439680261,
            -1004479057531,
            -1003733380888,
            -1003648174454,
            -1003602438273,
            -1003750876947,
            -1003755971890,
            -1003562083930,
            -1003510781166,
            -1003949102825,
            -1003952468268,
            -1003957014774,
            -1003963418462,
            -1003974009699,
            -1003968999841,
            -1004039908324,
            -1004275694663,
            -1004290908890,
            -1003745381942,
            -1003781300475,
            -1003794009872,
        ],
    },
    {
        "name": "Bot_6",
        "token": "8859111207:AAHOfc_nuwr-ypCS1gQZ8sT8NB4fw2Pki5k",
        "source_idx": 1,
        "destinations": [
            -1003896595539,
            -1003892664718,
            -1003891885147,
            -1003891493525,
            -1003877302321,
            -1003945892471,
            -1003941980188,
            -1003937035229,
            -1003935065494,
            -1003932662806,
            -1003910090206,
            -1003908852473,
            -1003902198631,
            -1003902077625,
            -1003876716517,
            -1003798360918,
            -1003909872909,
            -1003935791509,
            -1003934694555,
            -1003924032461,
            -1003923259421,
            -1003911098979,
            -1003908764958,
            -1003905849530,
            -1003903813483,
            -1003937605594,
            -1003940952632,
            -1003941324372,
            -1003946456644,
        ],
    },
    {
        "name": "Bot_7",
        "token": "8968176107:AAFV3swDJcXH8uYmjVtzq7yvGlhnwG1wKeE",
        "source_idx": 1,
        "destinations": [
            -1003819237693,
            -1003811802238,
            -1003805236818,
            -1003805024761,
            -1003800584850,
            -1003798597596,
            -1003795511929,
            -1004240679985,
            -1003998779359,
            -1003988563148,
            -1003946791321,
            -1003717995460,
            -1003769931828,
            -1003789922298,
            -1003515320628,
            -1003527701097,
            -1003585085457,
            -1003587316345,
            -1003605031669,
            -1003769878315,
            -1003752448700,
            -1003743520807,
            -1003738805571,
            -1003724801416,
            -1003714917243,
            -1003871499261,
            -1003865637738,
            -1003857187186,
            -1003724355192,
        ],
    },
    {
        "name": "Bot_8",
        "token": "8975943928:AAFBvdB3GrHOzcYXDVm14bcEDsuiOb3QBkc",
        "source_idx": 1,
        "destinations": [
            -1003947738607,
            -1003473669387,
            -1003394812659,
            -1002961388909,
            -1002949018087,
            -1002940926130,
            -1002908577068,
            -1002784545607,
            -1002737949654,
            -1002688227640,
            -1002646112149,
            -1003710584803,
            -1003704392849,
            -1003682206707,
            -1003635901925,
            -1003617023401,
            -1003951329028,
            -1003954176519,
            -1003957903651,
            -1003960747779,
            -1003976422123,
            -1003985879962,
            -1003992516914,
            -1003998709852,
            -1002929094283,
            -1003588125898,
            -1004364840257,
            -1004336110077,
            -1003936185379,
        ],
    },
    {
        "name": "Bot_9",
        "token": "8879023715:AAHGeLz3UgjjOxFGM2YfJmpoWuTzA5PPyus",
        "source_idx": 2,
        "destinations": [
            -1003919403109,
            -1004379687174,
            -1004449217757,
            -1003988283406,
            -1004413672815,
        ],
    },
    {
        "name": "Bot_10",
        "token": "8924069980:AAG5hybPPX5pvhtLVBV8RvM5Tr7EvsjiSMw",
        "source_idx": 2,
        "destinations": [
            -1004458528166,
            -1004440230647,
            -1004333406448,
            -1003911474076,
        ],
    },
]


async def process_and_send(client, bot_info):
  correct_source = SOURCES[bot_info["source_idx"]]

  limit_count = (
      1
      if bot_info["name"] in ["Bot_9", "Bot_10"] or "9" in bot_info["name"]
      else 10
  )

  try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT id, msg_id FROM message_queue WHERE source_chat = ? LIMIT ?",
        (correct_source, limit_count),
    )
    rows = c.fetchall()

    if not rows:
      conn.close()
      return

    row_ids = [row[0] for row in rows]
    post_ids = [row[1] for row in rows]

    for dest in bot_info["destinations"]:
      for msg_id in post_ids:
        try:
          # Source message fetch karenge taaki media aur original text mil sake
          orig_msg = await client.get_messages(correct_source, ids=msg_id)
          if not orig_msg:
            continue

          # Original text/caption ke sath footer jorenge
          orig_text = orig_msg.text or ""
          combined_text = (
              f"{orig_text}\n\n{FOOTER_TEXT}"
              if orig_text
              else f"{FOOTER_TEXT}"
          )

          if orig_msg.media:
            # Agar media hai (photo/video), toh media ke sath combined caption bhejenge
            await client.send_file(
                dest,
                orig_msg.media,
                caption=combined_text,
                link_preview=False,
            )
          else:
            # Agar sirf text message hai
            await client.send_message(
                dest, combined_text, link_preview=False
            )

        except Exception as e:
          logging.error(f"Error sending to {dest}: {e}")

    c.executemany(
        "DELETE FROM message_queue WHERE id = ?", [(rid,) for rid in row_ids]
    )
    conn.commit()
    conn.close()
    logging.info(
        f"Successfully processed batch with embedded caption footer for"
        f" {bot_info['name']}"
    )

  except Exception as e:
    logging.error(f"Database error in {bot_info['name']}: {e}")


async def main():
  init_db()
  clients = []

  for idx, data in enumerate(BOTS_DATA):
    client = TelegramClient(f"session_{data['name']}", API_ID, API_HASH)
    await client.start(bot_token=data["token"])

    assigned_source = SOURCES[data["source_idx"]]

    if data["name"] in ["Bot_1", "Bot_5", "Bot_9"]:

      @client.on(events.NewMessage(chats=assigned_source))
      async def handler(event, b_info=data):
        try:
          conn = sqlite3.connect(DB_NAME)
          c = conn.cursor()
          c.execute(
              "INSERT OR IGNORE INTO message_queue (msg_id, source_chat) VALUES"
              " (?, ?)",
              (event.id, event.chat_id),
          )
          conn.commit()
          conn.close()
          logging.info(
              f"[{b_info['name']}] Saved new post ID {event.id} from source"
              f" {event.chat_id} to queue."
          )
        except Exception as e:
          logging.error(f"Error saving to queue: {e}")

    clients.append((client, data))
    logging.info(
        f"🚀 {data['name']} started successfully and listening to source"
        f" {assigned_source}!"
    )

  scheduler = AsyncIOScheduler()

  for index in range(8):
    bot_client, bot_info = clients[index]

    async def hourly_job_task(c=bot_client, info=bot_info):
      await process_and_send(c, info)

    scheduler.add_job(hourly_job_task, "cron", minute="0")

  for index in [8, 9]:
    bot_client, bot_info = clients[index]

    async def bulk_job_task(c=bot_client, info=bot_info):
      await process_and_send(c, info)

    scheduler.add_job(
        bulk_job_task, "cron", minute="0,6,12,18,24,30,36,42,48,54"
    )

  scheduler.start()
  logging.info("Scheduler running with embedded caption footer...")

  await asyncio.gather(
      *(client.run_until_disconnected() for client, _ in clients)
  )


if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print("Bots stopped safely.")
