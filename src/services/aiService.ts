import { graphqlMutation, graphqlQuery } from "@/lib/graphqlClient";
import {
  AI_CHAT_DETAIL_QUERY,
  AI_CHATS_QUERY,
  AI_CREATE_CHAT,
  AI_SEND_MESSAGE,
} from "@/graphql/adminOperations";

export const aiService = {
  chats: (limit = 50, offset = 0) =>
    graphqlQuery(AI_CHATS_QUERY, {
      filters: { limit, offset },
    }),

  chat: (chatId: string) => graphqlQuery(AI_CHAT_DETAIL_QUERY, { chatId }),

  createChat: (title?: string) =>
    graphqlMutation(AI_CREATE_CHAT, {
      input: { ...(title ? { title } : {}) },
    }),

  sendMessage: (chatId: string, message: string) =>
    graphqlMutation(AI_SEND_MESSAGE, {
      chatId,
      input: { message },
    }),
};
