import Image from "next/image";
import logo from "@/app/assets/icons/logo.svg";

export function RoastMark({
  className,
  width = 35,
  height = 39,
}: {
  className?: string;
  width?: number;
  height?: number;
}) {
  return (
    <Image src={logo} alt="" aria-hidden width={width} height={height} className={className} />
  );
}
