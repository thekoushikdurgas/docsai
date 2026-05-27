import { graphqlMutation, graphqlQuery } from "@/lib/graphqlClient";
import {
  KNOWLEDGE_ARTICLES_FULL_QUERY,
  KNOWLEDGE_CREATE_ARTICLE,
  KNOWLEDGE_DELETE_ARTICLE,
  KNOWLEDGE_UPDATE_ARTICLE,
} from "@/graphql/adminOperations";

export const knowledgeService = {
  list: (limit = 50, offset = 0) =>
    graphqlQuery(KNOWLEDGE_ARTICLES_FULL_QUERY, { limit, offset }),

  create: (title: string, body: string, tags: string[] = []) =>
    graphqlMutation(KNOWLEDGE_CREATE_ARTICLE, {
      input: { title, body, tags },
    }),

  update: (articleId: string, title?: string, body?: string, tags?: string[]) =>
    graphqlMutation(KNOWLEDGE_UPDATE_ARTICLE, {
      input: {
        articleId,
        ...(title !== undefined ? { title } : {}),
        ...(body !== undefined ? { body } : {}),
        ...(tags !== undefined ? { tags } : {}),
      },
    }),

  delete: (articleId: string) =>
    graphqlMutation(KNOWLEDGE_DELETE_ARTICLE, { articleId }),
};
