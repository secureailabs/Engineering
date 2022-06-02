import React from 'react';

import Feed from '@secureailabs/web-ui/components/Feed';

import TimeAgo from 'javascript-time-ago';

import en from 'javascript-time-ago/locale/en.json';
TimeAgo.addLocale(en);
const timeAgo = new TimeAgo('en');

import { TFeedSuccessProps } from './Feed.types';

import { useNavigate } from 'react-router';

import _ from 'lodash';

const FeedSuccess: React.FC<TFeedSuccessProps> = ({
  getAllFeedsData,
  limit,
  containerHeight,
}) => {
  const navigate = useNavigate();
  const parsed_data = Object.entries(getAllFeedsData.Feeds)
    .map(([key, value]) => {
      return {
        title: value.Title,
        description: value.Description,
        date: timeAgo.format(value.CreatedAt),
        image: value.Image,
        avatar: value.avatar,
        avatar_color: value.avatar_color,
      };
    })
    .slice(0, limit);
  return (
    <Feed
      title="Feed"
      seconday="Show all"
      containerHeight={containerHeight}
      //@ts-ignore
      feed={_.sortBy(parsed_data, 'date')}
    />
  );
};

export default FeedSuccess;
