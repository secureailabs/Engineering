import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  putUpdateAccessRightsStart,
  putUpdateAccessRightsReset,
} from '@redux/accountManager/accountManager.actions';
import UpdateAccessRights from './UpdateAccessRights.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { selectAccountManager } from '@redux/accountManager/accountManager.selectors';
import { selectUser } from '@redux/user/user.selectors';
import { TPutUpdateAccessRightsStart } from '@redux/accountManager/accountManager.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    putUpdateAccessRightsError: selectAccountManager(state)
      .putUpdateAccessRightsError,
    putUpdateAccessRightsState: selectAccountManager(state)
      .putUpdateAccessRightsState,
    putUpdateAccessRightsData: selectAccountManager(state)
      .putUpdateAccessRightsData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  // putUpdateAccessRightsStart: (data: TGetUpdateAccessRightsStart) => dispatch(putUpdateAccessRightsStart(data)),
  putUpdateAccessRightsStart: (data: TPutUpdateAccessRightsStart) =>
    dispatch(putUpdateAccessRightsStart(data)),
  putUpdateAccessRightsReset: () => dispatch(putUpdateAccessRightsReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  // @ts-ignore
  UpdateAccessRights
);
