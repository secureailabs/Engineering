import { UseMutateFunction } from "react-query";
import { IUserData } from "@redux/user/user.typeDefs"

export type TDashboardProps = {
    userData: IUserData;
    logoutMutationFunction: UseMutateFunction<void, unknown, void, unknown>;
}