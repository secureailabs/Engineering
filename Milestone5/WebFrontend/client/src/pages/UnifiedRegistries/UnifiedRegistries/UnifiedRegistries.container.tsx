import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getAllUnifiedRegistriesStart,
  getAllUnifiedRegistriesReset,
} from '@redux/unifiedRegistry/unifiedRegistry.actions';
import { selectUnifiedRegistry } from '@redux/unifiedRegistry/unifiedRegistry.selector';
import { selectUser } from '@redux/user/user.selectors';
import UnifiedRegistries from './UnifiedRegistries.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';

const mapStateToProps = (state: IState) => {
  return {
    getAllUnifiedRegistriesError: selectUnifiedRegistry(state)
      .getAllUnifiedRegistriesError,
    getAllUnifiedRegistriesState: selectUnifiedRegistry(state)
      .getAllUnifiedRegistriesState,
    getAllUnifiedRegistriesData: selectUnifiedRegistry(state)
      .getAllUnifiedRegistriesData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  getAllUnifiedRegistriesStart: () => dispatch(getAllUnifiedRegistriesStart()),
  getAllUnifiedRegistriesReset: () => dispatch(getAllUnifiedRegistriesReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  //@ts-ignore
  UnifiedRegistries
);
