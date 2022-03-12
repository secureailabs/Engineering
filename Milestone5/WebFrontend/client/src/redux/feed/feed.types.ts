import { TDatasetSuccessProps } from '@pages/Datasets/Dataset/Dataset.types';
import { TGetDatasetSuccess } from '../dataset/dataset.typeDefs';

export type TPostFeedStart = {
  Name: string;
  Description: string;
};
export type TPostFeedSuccess = null;

export type TDeleteFeedStart = {
  ID: string;
};
export type TDeleteFeedSuccess = null;

export type TGetAllFeedsStart = {};

export type TGetAllFeedsSuccess = {
  Feeds: Record<string, TGetFeedSuccess['Feed']>;
};

export type TGetFeedSuccess = {
  Feed: {
    ID: string;
    Title: string;
    Description: string;
    Image: string;
    CreatedAt: Date;
    UpdatedAt: Date;
    Link?: string;
    avatar?: string;
    avatar_color?: string;
  };
};

export type TGetFeedStart = {
  ID: string;
};

export type TPutFeedSuccess = null;

export type TPutFeedStart = {
  ID: string;
};
