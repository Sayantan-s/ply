import winston from "winston";
import crypto from "node:crypto";

const logger = winston.createLogger({
  level: "info",
  format: winston.format.combine(
    winston.format.colorize({ all: true }),
    winston.format.label({ label: "[LOGGER]" }),
    winston.format.timestamp({ format: "YY-MM-DD HH:MM:SS" }),
    winston.format.printf(
      (info) => ` ${info.label} ${info.timestamp}  ${info.level} : ${info.message}`,
    ),
  ),
  transports: [new winston.transports.Console()],
});

export class Logging {
  id: string;
  logger: winston.Logger;
  private static instance: Logging | undefined;
  constructor(loggerId?: string) {
    this.id = loggerId || crypto.randomUUID();
    this.logger = logger.child({ requestId: this.id });
  }

  static get client() {
    if (!Logging.instance?.id) Logging.instance = new Logging();
    return Logging.instance;
  }

  init(loggerId: string) {
    Logging.instance = new Logging(loggerId);
  }
}
