import React from 'react';
import Button from '@components/Button';
import SingleFormViewBG from '@assets/SingleFormViewBG.png';
import type { TLoginLinkView } from './LoginLinkView.types';

const LoginLinkView: React.FC<TLoginLinkView> = (props) => {

  return (
    <div className="loginlinkview" style={{backgroundImage: `url(${SingleFormViewBG})`}}>
      <div className="loginlinkview__message">{props.message}</div>
      <div className="loginview__button">
        <Button
          onClick={props.onClick}
        >
          {/* @ts-ignore */}
          {'buttonText' in props ? props.buttonText:<>Login</>}
        </Button>
      </div>
    </div>
      );
};

export default LoginLinkView;
