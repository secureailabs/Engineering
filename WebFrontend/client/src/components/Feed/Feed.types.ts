import { TGetAllFeedsSuccess } from '@redux/feed/feed.types';
import { IUserData } from '@redux/user/user.typeDefs';
import { IDefaults } from '@redux/typedefs';

export type TFeedProps = {
  getAllFeedsStart(): void;
  getAllFeedsReset(): void;
  getAllFeedsState: IDefaults['state'];
  getAllFeedsData: TGetAllFeedsSuccess;
  limit?: number;
  containerHeight?: boolean;
};

export type TFeedSuccessProps = {
  getAllFeedsData: TGetAllFeedsSuccess;
  limit?: number;
  containerHeight?: boolean;
};
