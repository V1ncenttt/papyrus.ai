import { Button as ShadBtn } from "@/components/ui/button"
export default function Button({ startIcon, btnText, onClick }) {
  return (
    <ShadBtn variant="softdark" size="lg" onClick={onClick}>
      {startIcon} <span className="inter-extraBold">{btnText}</span>
    </ShadBtn>
  )
}
