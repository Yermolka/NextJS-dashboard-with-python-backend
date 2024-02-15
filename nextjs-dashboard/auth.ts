import NextAuth from "next-auth";
import { authConfig } from "./auth.config";
import credentials from "next-auth/providers/credentials";
import { z } from "zod";
import type { User } from "./app/lib/definitions";
import bcrypt from 'bcrypt';

async function getUser(email: string): Promise<User | undefined> {
    try {
        const resp = await fetch(`${process.env.USERS_API_URL}/users/${email}`);
        if (resp.status != 200) {
            return undefined;
        }
        const data = await resp.json() as User;
        return data;
    } catch (error) {
        console.error(error);
        throw new Error('Users API Error');
    }
}

export const { auth, signIn, signOut } = NextAuth({
    ...authConfig,
    providers: [
        credentials({
            async authorize(credentials) {
                const parsedCredentials = z
                    .object({ email: z.string().email(), password: z.string().min(6) })
                    .safeParse(credentials);

                if (parsedCredentials.success) {
                    const { email, password } = parsedCredentials.data;
                    const user = await getUser(email);
                    if (!user) return null;
                    const passwordMatch = await bcrypt.compare(password, user.password);
                    // const passwordMatch = password === user.password;
                    if (passwordMatch) return user;
                }
                console.log('Invalid credentials');
                return null;
            },
        }),
    ],
});