import React from 'react';

import Feed from '@secureailabs/web-ui/components/Feed';

import TimeAgo from 'javascript-time-ago';

import en from 'javascript-time-ago/locale/en.json';
TimeAgo.addLocale(en);
const timeAgo = new TimeAgo('en');

import { TFeedSuccessProps } from './Feed.types';

const FeedSuccess: React.FC<TFeedSuccessProps> = ({
  getAllFeedsData,
  limit,
  containerHeight,
}) => {
  const parsed_data = Object.entries(getAllFeedsData.Feeds)
    .map(([key, value]) => {
      return {
        title: value.Title,
        description: value.Description,
        image: value.Image,
        date: timeAgo.format(value.CreatedAt),
      };
    })
    .slice(0, limit);
  return (
    <Feed
      title="Feed"
      seconday="Show all"
      containerHeight={containerHeight}
      //@ts-ignore
      feed={parsed_data}
    />
  );
};

export default FeedSuccess;
