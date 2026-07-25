import { Bot } from "grammy";
import { logger } from "./lib/logger";

const token = process.env["TELEGRAM_BOT_TOKEN"];

if (!token) {
  throw new Error("TELEGRAM_BOT_TOKEN environment variable is required.");
}

const bot = new Bot(token);

const API_BASE = "https://ankan-dey-number-search-api.hf.space/search";
const API_KEY = "Demo";

// Escape special HTML characters so the message never breaks Telegram HTML mode
function esc(text: string | undefined | null): string {
  if (!text || text === "N/A") return "N/A";
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

interface ApiData {
  num?: string;
  name?: string;
  fname?: string;
  aadhar?: string;
  address?: string;
  circle?: string;
  email?: string;
  alt?: string;
  [key: string]: unknown;
}

interface ApiResponse {
  status: string;
  data?: ApiData[];
  [key: string]: unknown;
}

async function fetchUserData(mobile: string): Promise<ApiData | null> {
  const url = `${API_BASE}?api_key=${API_KEY}&mobile=${encodeURIComponent(mobile)}`;
  const res = await fetch(url);
  if (!res.ok) return null;
  const json = (await res.json()) as ApiResponse;
  if (json.status !== "success" || !json.data || json.data.length === 0) return null;
  return json.data[0] ?? null;
}

function formatMessage(mobile: string, d: ApiData): string {
  return (
    `╔══════════════════════════════╗\n` +
    `       🔍 USER DETAILS FOUND\n` +
    `╚══════════════════════════════╝\n\n` +
    `📱 <b>Number Searched:</b> <code>${esc(mobile)}</code>\n\n` +
    `👤 <b>Full Name:</b> ${esc(d.name)}\n` +
    `👨 <b>Father's Name:</b> ${esc(d.fname)}\n` +
    `🪪 <b>Aadhar Number:</b> <code>${esc(d.aadhar)}</code>\n` +
    `📍 <b>Address:</b> ${esc(d.address)}\n` +
    `📡 <b>Circle / Operator:</b> ${esc(d.circle)}\n` +
    `📧 <b>Email:</b> ${esc(d.email)}\n` +
    `📞 <b>Alt. Number:</b> ${esc(d.alt)}\n\n` +
    `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n` +
    `⚠️ <b>DISCLAIMER:</b>\n` +
    `<i>These are FAKE details, NOT real information.</i>\n` +
    `<i>Only made for PRANKING people.</i>\n` +
    `<i>Do NOT use for any illegal or harmful activity.</i>\n\n` +
    `👨‍💻 <b>Developer:</b> MADARA DEFAULTER\n` +
    `🏷️ <b>Credits:</b> MADARA X BRAND\n` +
    `🔗 <b>Group Link:</b> <a href="https://t.me/+gqpAcHXgggxhZjRl">Join Here</a>\n\n` +
    `🗑️ <i>This message will self-destruct in 2 minutes...</i>`
  );
}

bot.command("start", (ctx) =>
  ctx.reply(
    `👋 <b>Welcome to the Prank Details Bot!</b>\n\n` +
    `Send me any mobile number and I'll fetch "details" of that person 😈\n\n` +
    `📌 <b>How to use:</b>\nJust type a number like:\n<code>6204864732</code>\n\n` +
    `Powered by <b>MADARA DEFAULTER 🔥</b>\n` +
    `Group: <a href="https://t.me/+gqpAcHXgggxhZjRl">MADARA X BRAND</a>`,
    { parse_mode: "HTML" }
  )
);

bot.command("help", (ctx) =>
  ctx.reply(
    `📖 <b>Help Menu</b>\n\n` +
    `Send any mobile number and the bot will fetch details for pranking your friends!\n\n` +
    `Example: <code>6204864732</code>\n\n` +
    `⚠️ All shown details are labelled as FAKE — for prank purposes only.\n\n` +
    `Powered by <b>MADARA DEFAULTER 🔥</b>`,
    { parse_mode: "HTML" }
  )
);

bot.on("message:text", async (ctx) => {
  const text = ctx.message.text.trim();

  // Accept 7–15 digit numbers, optionally prefixed with + or country code spaces/dashes
  const phonePattern = /^[+]?[\d\s\-().]{7,15}$/;
  if (!phonePattern.test(text)) {
    await ctx.reply(
      `❌ <b>Invalid input!</b>\n\nPlease send a valid mobile number.\nExample: <code>6204864732</code>`,
      { parse_mode: "HTML" }
    );
    return;
  }

  const cleanNumber = text.replace(/[\s\-().+]/g, "");

  // Send "searching" indicator
  const searchMsg = await ctx.reply(`🔍 <b>Searching database...</b>`, {
    parse_mode: "HTML",
  });

  let data: ApiData | null = null;
  try {
    data = await fetchUserData(cleanNumber);
  } catch (err) {
    logger.warn({ err }, "API fetch error");
  }

  // Delete the searching message
  try {
    await ctx.api.deleteMessage(ctx.chat.id, searchMsg.message_id);
  } catch {
    // ignore if already gone
  }

  if (!data) {
    await ctx.reply(
      `❌ <b>No data found</b> for <code>${esc(cleanNumber)}</code>.\n\nTry a different number.`,
      { parse_mode: "HTML" }
    );
    return;
  }

  const message = formatMessage(cleanNumber, data);
  const sentMsg = await ctx.reply(message, {
    parse_mode: "HTML",
    link_preview_options: { is_disabled: true },
  });

  logger.info({ chatId: ctx.chat.id, phone: cleanNumber }, "Sent prank details");

  // Auto-delete after 2 minutes (120,000 ms)
  setTimeout(async () => {
    try {
      await ctx.api.deleteMessage(ctx.chat.id, sentMsg.message_id);
      await ctx.reply(
        `🗑️ <i>Details for <code>${esc(cleanNumber)}</code> have been automatically deleted.</i>`,
        { parse_mode: "HTML" }
      );
    } catch (err) {
      logger.warn({ err }, "Failed to auto-delete prank message");
    }
  }, 120_000);
});

export function startBot(): void {
  bot.start({ drop_pending_updates: true });
  logger.info("Telegram prank bot started (long polling)");

  process.once("SIGINT", () => bot.stop());
  process.once("SIGTERM", () => bot.stop());
}
