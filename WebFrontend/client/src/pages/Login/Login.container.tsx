import { MutationFunction, useMutation, useQueryClient } from 'react-query';
import axios, { AxiosError } from 'axios';
import { axiosProxy } from '@APIs/utils';
import { IEmailAndPassword } from '@APIs/user/user.typeDefs';
import Login from './Login.component';

const LoginContainer: React.FC = () => {
  const post = async (data: IEmailAndPassword): Promise<IEmailAndPassword> => {
    const res = await axios.post<IEmailAndPassword>(
      `${axiosProxy()}/api/v1/login`,
      // @ts-ignore
      new URLSearchParams(data),
      {
        withCredentials: true,
      });
    return res.data;
  }

  const queryClient = useQueryClient()
  //@ts-ignore
  const loginMutation = useMutation<IEmailAndPassword, AxiosError>(post, { onSuccess: () => queryClient.invalidateQueries('userData') });


  return Login({ signInStart: loginMutation.mutate, signInReset: loginMutation.reset, status: loginMutation.status })
}

export default LoginContainer
