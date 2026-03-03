import Redis from "ioredis";
import { Logging } from "../utils/logging";

let redisClient: Redis | null = null;

export const getRedisClient = () => {
  if (!redisClient) {
    const config = useRuntimeConfig();

    redisClient = new Redis(config.REDIS_URL as string);

    redisClient.once("connect", () => {
      Logging.client.logger.info("Redis client connected...");
    });

    redisClient.once("ready", () => {
      Logging.client.logger.info("Redis client ready...");
    });

    redisClient.once("error", (err) => {
      Logging.client.logger.error(`Redis client error: ${JSON.stringify(err)}`, err);
    });

    redisClient.ping().catch((err) => {
      Logging.client.logger.error(`Redis ping error: ${JSON.stringify(err)}`, err);
    });
  }
  return redisClient;
};

export const disconnectRedis = () => {
  if (redisClient) {
    redisClient.disconnect();
    redisClient = null;
    Logging.client.logger.info("Redis client disconnected...");
  }
};
