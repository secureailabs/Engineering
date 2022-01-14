import { connect } from 'react-redux';
import { compose, Dispatch } from 'redux';

import {
  getOrganizationStart,
  getOrganizationReset,
} from '@redux/organization/organization.actions';
import Organization from './Organization.component';
import { IState } from '@redux/root-reducer';
import { RootAction } from '@redux/root.types';
import { selectOrganization } from '@redux/organization/organization.selectors';
import { selectUser } from '@redux/user/user.selectors';

const mapStateToProps = (state: IState) => {
  return {
    getOrganizationError: selectOrganization(state).getOrganizationError,
    getOrganizationState: selectOrganization(state).getOrganizationState,
    getOrganizationData: selectOrganization(state).getOrganizationData,
    userData: selectUser(state).userData,
  };
};

//trying to remove func from dispatch functions

const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
  // getOrganizationStart: (data: TGetOrganizationStart) => dispatch(getOrganizationStart(data)),
  getOrganizationStart: (key: string) => dispatch(getOrganizationStart()),
  getOrganizationReset: () => dispatch(getOrganizationReset()),
});

export default compose(connect(mapStateToProps, mapDispatchToProps))(
  // @ts-ignore
  Organization
);
