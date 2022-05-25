import { useMutation, useQueryClient } from 'react-query';

import { logout } from '@redux/user/user.utils';

import Dashboard from './Dashboard.component';


const DashboardContainer: React.FC = () => {
  const queryClient = useQueryClient()
  const logoutMutation = useMutation(logout, { onSettled: () => { queryClient.invalidateQueries('userData');
 console.log(queryClient.getQueryData('userData'))}, retry: false })

  return Dashboard({userData : queryClient.getQueryData('userData'), logoutMutationFunction : logoutMutation.mutate})
}

export default DashboardContainer