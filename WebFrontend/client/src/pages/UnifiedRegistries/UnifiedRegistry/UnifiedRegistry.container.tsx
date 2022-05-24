import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getUnifiedRegistryStart,
  getUnifiedRegistryReset,
} from '@app/redux/unifiedRegistry/unifiedRegistry.actions';
import { selectUnifiedRegistry } from '@app/redux/unifiedRegistry/unifiedRegistry.selector';
import { selectUser } from '@app/redux/user/user.selectors';
import UnifiedRegistry from './UnifiedRegistry.component';
import { IState } from '@app/redux/root-reducer';
import { RootAction } from '@app/redux/root.types';
import { TGetUnifiedRegistryStart } from '@app/redux/unifiedRegistry/unifiedRegistry.types';

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
