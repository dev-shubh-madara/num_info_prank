import { Telegraf, Context } from "telegraf";
import { faker } from "@faker-js/faker";
import { logger } from "./lib/logger";

const token = process.env["TELEGRAM_BOT_TOKEN"];

if (!token) {
  throw new Error("TELEGRAM_BOT_TOKEN environment variable is required.");
}

const bot = new Telegraf(token);

function generateFakeProfile(phoneNumber: string) {
  // Seed faker with the phone number so output is consistent per number per session
  const seed = phoneNumber.replace(/\D/g, "").split("").reduce((acc, d) => acc + d.charCodeAt(0), 0);
  faker.seed(seed + Date.now()); // Add Date.now() for randomness each call

  const gender = faker.person.sexType();
  const firstName = faker.person.firstName(gender);
  const lastName = faker.person.lastName();
  const age = faker.number.int({ min: 18, max: 60 });
  const city = faker.location.city();
  const country = faker.location.country();
  const email = faker.internet.email({ firstName, lastName });
  const job = faker.person.jobTitle();
  const company = faker.company.name();
  const address = faker.location.streetAddress(true);
  const dob = faker.date.birthdate({ min: age, max: age, mode: "age" }).toDateString();
  const bloodGroup = faker.helpers.arrayElement(["A+", "A−", "B+", "B−", "AB+", "AB−", "O+", "O−"]);
  const education = faker.helpers.arrayElement([
    "Bachelor's in Computer Science",
    "Master's in Business Administration",
    "Bachelor's in Engineering",
    "Diploma in Arts",
    "Bachelor's in Commerce",
    "Master's in Psychology",
    "PhD in Physics",
    "Bachelor's in Law",
  ]);
  const maritalStatus = faker.helpers.arrayElement(["Single", "Married", "Divorced", "Widowed"]);
  const altPhone = faker.phone.number({ style: "international" });
  const ip = faker.internet.ipv4();
  const bankBalance = faker.finance.amount({ min: 500, max: 500000, dec: 2, symbol: "₹" });
  const socialMedia = `@${faker.internet.username({ firstName, lastName }).toLowerCase()}`;

  return {
    firstName,
    lastName,
    gender: gender === "male" ? "Male" : "Female",
    age,
    dob,
    phone: phoneNumber,
    altPhone,
    email,
    address,
    city,
    country,
    job,
    company,
    education,
    maritalStatus,
    bloodGroup,
    ip,
    bankBalance,
    socialMedia,
  };
}

function formatMessage(profile: ReturnType<typeof generateFakeProfile>): string {
  return `
╔══════════════════════════════╗
       🔍 USER DETAILS FOUND
╚══════════════════════════════╝

📱 *Number Searched:* \`${profile.phone}\`

👤 *Full Name:* ${profile.firstName} ${profile.lastName}
🚻 *Gender:* ${profile.gender}
🎂 *Date of Birth:* ${profile.dob}
🔢 *Age:* ${profile.age} years
💉 *Blood Group:* ${profile.bloodGroup}
💍 *Marital Status:* ${profile.maritalStatus}

📞 *Alt. Phone:* ${profile.altPhone}
📧 *Email:* ${profile.email}
📍 *Address:* ${profile.address}
🏙️ *City:* ${profile.city}
🌍 *Country:* ${profile.country}

💼 *Job Title:* ${profile.job}
🏢 *Company:* ${profile.company}
🎓 *Education:* ${profile.education}

💰 *Bank Balance:* ${profile.bankBalance}
🌐 *IP Address:* ${profile.ip}
📲 *Social Media:* ${profile.socialMedia}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ *DISCLAIMER:*
_These are FAKE details, NOT real information._
_This data is generated only for PRANKING purposes._
_Do NOT use for any illegal or harmful activity._

🔥 *API Owner:* MADARA DEFAULTER

🗑️ _This message will self-destruct in 2 minutes..._
`.trim();
}

bot.start((ctx) => {
  ctx.reply(
    `👋 *Welcome to the Prank Details Bot!*\n\n` +
    `Send me any phone number and I'll fetch "details" of that person 😈\n\n` +
    `📌 *How to use:*\nJust type a phone number like:\n\`+919876543210\`\n\nPowered by *MADARA DEFAULTER* 🔥`,
    { parse_mode: "Markdown" }
  );
});

bot.help((ctx) => {
  ctx.reply(
    `📖 *Help Menu*\n\n` +
    `Just send any phone number and I'll prank your friends with fake details!\n\n` +
    `Example: \`+919876543210\`\n\n` +
    `⚠️ All details are 100% FAKE and for prank purposes only.\n\n` +
    `Powered by *MADARA DEFAULTER* 🔥`,
    { parse_mode: "Markdown" }
  );
});

// Handle any text that looks like a phone number
bot.on("text", async (ctx: Context) => {
  const text = ctx.message && "text" in ctx.message ? ctx.message.text.trim() : "";

  // Basic phone number pattern check
  const phonePattern = /^[+]?[\d\s\-().]{7,20}$/;

  if (!phonePattern.test(text)) {
    await ctx.reply(
      `❌ Invalid input!\n\nPlease send a valid phone number.\nExample: \`+919876543210\``,
      { parse_mode: "Markdown" }
    );
    return;
  }

  const cleanNumber = text.replace(/[\s\-().]/g, "");

  // Send "searching" indicator
  const searchMsg = await ctx.reply(`🔍 *Searching database...*`, { parse_mode: "Markdown" });

  // Simulate a fetch delay
  await new Promise((resolve) => setTimeout(resolve, 1500));

  const profile = generateFakeProfile(cleanNumber);
  const message = formatMessage(profile);

  // Delete the searching message
  try {
    await ctx.deleteMessage(searchMsg.message_id);
  } catch {
    // ignore if already deleted
  }

  // Send the fake details
  const sentMsg = await ctx.reply(message, { parse_mode: "Markdown" });

  logger.info({ chatId: ctx.chat?.id, phone: cleanNumber }, "Sent prank details");

  // Auto-delete after 2 minutes (120,000 ms)
  setTimeout(async () => {
    try {
      await ctx.deleteMessage(sentMsg.message_id);
      await ctx.reply(
        `🗑️ _The details for \`${cleanNumber}\` have been automatically deleted._`,
        { parse_mode: "Markdown" }
      );
    } catch (err) {
      logger.warn({ err }, "Failed to auto-delete prank message");
    }
  }, 120_000);
});

export function startBot(): void {
  bot.launch({ dropPendingUpdates: true });
  logger.info("Telegram prank bot started (long polling)");

  process.once("SIGINT", () => bot.stop("SIGINT"));
  process.once("SIGTERM", () => bot.stop("SIGTERM"));
}
