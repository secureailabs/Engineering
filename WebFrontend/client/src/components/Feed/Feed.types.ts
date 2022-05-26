import { TGetAllFeedsSuccess } from '@APIs/feed/feed.types';
import { IUserData } from '@APIs/user/user.typeDefs';
import { IDefaults } from '@APIs/typedefs';

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
