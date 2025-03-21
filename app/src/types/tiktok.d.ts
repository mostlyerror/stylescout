export interface TikTokAuthResponse {
  access_token: string;
  expires_in: number;
  open_id: string;
  refresh_token: string;
  refresh_expires_in: number;
  scope: string;
}

export interface TikTokVideo {
  id: string;
  title: string;
  cover_url: string;
  share_url: string;
  create_time: number;
  author: {
    id: string;
    username: string;
    display_name: string;
    avatar_url: string;
  };
}

export interface TikTokSearchResponse {
  data: {
    videos: TikTokVideo[];
    cursor: number;
    has_more: boolean;
  };
  error: {
    code: number;
    message: string;
  } | null;
}

export interface TikTokCommentResponse {
  data: {
    comment_id: string;
  };
  error: {
    code: number;
    message: string;
  } | null;
} 