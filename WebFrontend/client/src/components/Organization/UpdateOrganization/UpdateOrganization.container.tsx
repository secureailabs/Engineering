import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  putOrganizationStart,
  putOrganizationReset,
  getOrganizationStart,
} from '@redux/organization/organization.actions';
import UpdateOrganization from './UpdateOrganization.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { selectOrganization } from '@redux/organization/organization.selectors';
import { selectUser } from '@redux/user/user.selectors';
import { TPutOrganizationStart } from '@redux/organization/organization.typeDefs';

const mapStateToProps = (state: IState) => {
  return {
    putOrganizationError: selectOrganization(state).putOrganizationError,
    putOrganizationState: selectOrganization(state).putOrganizationState,
    putOrganizationData: selectOrganization(state).putOrganizationData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  // putOrganizationStart: (data: TGetOrganizationStart) => dispatch(putOrganizationStart(data)),
  putOrganizationStart: (data: TPutOrganizationStart) =>
    dispatch(putOrganizationStart(data)),
  putOrganizationReset: () => dispatch(putOrganizationReset()),
  getOrganizationStart: () => dispatch(getOrganizationStart()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  // @ts-ignore
  UpdateOrganization
);
