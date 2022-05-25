import { UseMutateFunction } from "react-query";
import { IUserData } from "@APIs/user/user.typeDefs"

export type TDashboardProps = {
    userData: IUserData;
    logoutMutationFunction: UseMutateFunction<void, unknown, void, unknown>;
}