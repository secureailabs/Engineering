import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getUnifiedRegistryStart,
  getUnifiedRegistryReset,
} from '@redux/unifiedRegistry/unifiedRegistry.actions';
import { selectUnifiedRegistry } from '@redux/unifiedRegistry/unifiedRegistry.selector';
import { selectUser } from '@redux/user/user.selectors';
import UnifiedRegistry from './UnifiedRegistry.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { TGetUnifiedRegistryStart } from '@redux/unifiedRegistry/unifiedRegistry.types';

const mapStateToProps = (state: IState) => {
  return {
    getUnifiedRegistryError: selectUnifiedRegistry(state)
      .getUnifiedRegistryError,
    getUnifiedRegistryState: selectUnifiedRegistry(state)
      .getUnifiedRegistryState,
    getUnifiedRegistryData: selectUnifiedRegistry(state).getUnifiedRegistryData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  getUnifiedRegistryStart: (data: TGetUnifiedRegistryStart) =>
    dispatch(getUnifiedRegistryStart(data)),
  getUnifiedRegistryReset: () => dispatch(getUnifiedRegistryReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  //@ts-ignore
  UnifiedRegistry
);
