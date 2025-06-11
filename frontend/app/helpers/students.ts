export const fullName = (student: { first_name: string; last_name: string }) => {
    return `${student.first_name} ${student.last_name}`;
}