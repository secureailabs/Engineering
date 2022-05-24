import { TGetAllFeedsSuccess } from '@app/redux/feed/feed.types';
import { IUserData } from '@app/redux/user/user.typeDefs';
import { IDefaults } from '@app/redux/typedefs';

export type TFeedProps = {
  // getAllFeedsStart(): void;
  // getAllFeedsReset(): void;
  // getAllFeedsState: IDefaults['state'];
  // getAllFeedsData: TGetAllFeedsSuccess;
  limit?: number;
  containerHeight?: boolean;
};

export type TFeedSuccessProps = {
  getAllFeedsData: TGetAllFeedsSuccess;
  limit?: number;
  containerHeight?: boolean;
};
