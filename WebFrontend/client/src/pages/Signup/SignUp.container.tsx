// import { connect } from 'react-redux';
// import { compose, Dispatch } from 'redux';

// import { signUpStart, signUpReset } from '@app/redux/user/user.actions';
// import { selectUser } from '@app/redux/user/user.selectors';
// import SignUp from './SignUp.component';
// import { IState } from '@app/redux/root-reducer';
// import { RootAction } from '@app/redux/root.types';

// import { IPostUserStart } from '@APIs/user/user.typeDefs';

// const mapStateToProps = (state: IState) => {
//   return {
//     userError: selectUser(state).userError,
//     userState: selectUser(state).userState,
//   };
// };

// //trying to remove func from dispatch functions

// const mapDispatchToProps = (dispatch: Dispatch<RootAction>) => ({
//   signUpStart: (data: IPostUserStart) => dispatch(signUpStart(data)),
//   signUpReset: () => dispatch(signUpReset()),
// });

// export default compose(connect(mapStateToProps, mapDispatchToProps))(SignUp);
export { }
