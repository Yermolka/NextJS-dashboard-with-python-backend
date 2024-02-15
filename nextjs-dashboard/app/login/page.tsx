'use server';

import { ArrowRightIcon } from "@heroicons/react/20/solid";
import AcmeLogo from "../ui/acme-logo";
import { Button } from "../ui/button";
import LoginForm from "../ui/login-form";
import { redirect } from "next/navigation";

export default async function LoginPage() {
    return(
        <main className="flex items-center justify-center md:h-screen">
            <div className="relative mx-auto flex w-full max-w-[400px] flex-col space-y-2.5 p-4 md:-mt-32">
                <div className="flex h-20 w-full items-end rounded-lg bg-blue-500 p-3 md:h-36">
                    <div className="w-32 text-white md:w-36">
                        <AcmeLogo />
                    </div>
                </div>
                <LoginForm />
                <SignUpButton />
            </div>
        </main>
    )
}

async function SignUpButton() {
    'use server';
    return (
      <Button className="mt-4 w-full">
        Sign Up <ArrowRightIcon className="ml-auto h-5 w-5 text-gray-50" />
      </Button>
    );
  }