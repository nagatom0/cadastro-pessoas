export function formatApiError(detail: any): string {
  if (Array.isArray(detail)) {
    return detail
      .map((err: any) => {
        const cleanMsg = err.msg ? err.msg.replace("Value error, ", "") : "Erro de validação";
        return cleanMsg;
      })
      .join(", ");
  }
  if (typeof detail === "string") {
    return detail;
  }
  return "";
}