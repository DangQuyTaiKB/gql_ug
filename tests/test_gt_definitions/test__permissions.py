import pytest

queries = {
    "acprograms": {
        "read": """query($id: UUID!){ result: ById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: Page(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $name: String!, $type_id: UUID!, $group_id: UUID!, $licenced_group_id: UUID!) {
        result: programInsert(program: {id: $id, name: $name, typeId: $type_id, groupId: $group_id, licencedGroupId: $licenced_group_id}) {
            id
            msg
            result: program {
                id
                name
                nameEn
                type { id }
                subjects { id }
                students { id }
                grantsGroup { id }
                licencedGroup { id }
                createdby { id }
                changedby { id }
                rbacobject { id }
            }
        }
    }"""
    }, 
    "acclassifications": {
        "read": """query($id: UUID!){ result: acClassificationById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acClassificationPage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $date: DateTime!, $order: Int!
            $student_id: UUID!, $semester_id: UUID! 
            $classificationlevel_id: UUID!
        ) {
        result: programClassificationInsert(classification: {
                id: $id, date: $date, order: $order
                studentId: $student_id, semesterId: $semester_id,
                classificationlevelId: $classificationlevel_id
            }) {
            id
            msg
            result: classification {
                id
                lastchange
                date
                order
                student { id }
                semester { id }
                level { id }
            }
        }
    }"""        
    },

    "acclassificationlevels": {
        "read": """query($id: UUID!){ result: acClassificationLevelById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acClassificationLevelPage(skip: $skip, limit: $limit) { id } }""",
        "query": """mutation (
            $id: UUID!, $name: String!, $name_en: String
            ) {
        result: programClassificationTypeInsert(classificationType: 
            {
                id: $id, name: $name, nameEn: $name_en
            }) {
            id
            msg
            result: classificationType {
                id
                name
                nameEn
            }
        }
    }"""
    },

    "acclassificationtypes": {
        "read": """query($id: UUID!){ result: acClassificationTypeById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acClassificationTypePage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation (
            $id: UUID!, $name: String!, $name_en: String
            ) {
        result: programClassificationTypeInsert(classificationType: 
            {
                id: $id, name: $name, nameEn: $name_en
            }) {
            id
            msg
            result: classificationType {
                id
                name
                nameEn
            }
        }
    }"""
    }, 
    "aclessons": {
        "read": """query($id: UUID!){ result: acLessonById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acLessonPage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $topic_id: UUID!, $type_id: UUID! ) {
        result: programLessonInsert(lesson: {
                id: $id, 
                topicId: $topic_id, typeId: $type_id
            }) {
            id
            msg
            result: lesson {
                id
                lastchange

                count
                topic { id }
                type { id }
            }
        }
    }"""
    },     
    "aclessontypes": {
        "read": """query($id: UUID!){ result: acLessonTypeById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acLessonTypePage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation (
            $id: UUID!, $name: String!, $name_en: String
            ) {
        result: programLessonTypeInsert(lessonType: 
            {
                id: $id, name: $name, nameEn: $name_en
            }) {
            id
            msg
            result: lessonType {
                id
                name
                nameEn
            }
        }
    }"""
    },         
    "acprogramforms": {
        "read": """query($id: UUID!){ result: acProgramFormTypeById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acProgramFormTypePage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $name: String!, $name_en: String) {
        result: programFormTypeInsert(formType: {id: $id, name: $name, nameEn: $name_en}) {
            id
            msg
            result: programFormType {
                id
                lastchange
                name
                nameEn
            }
        }
    }"""
    },             
    "acprograms": {
        "read": """query($id: UUID!){ result: acProgramById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acProgramPage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $name: String!, $type_id: UUID!, $group_id: UUID!, $licenced_group_id: UUID!) {
        result: programInsert(program: {id: $id, name: $name, typeId: $type_id, groupId: $group_id, licencedGroupId: $licenced_group_id}) {
            id
            msg
            result: program {
                id
                name
                nameEn
                type { id }
                subjects { id }
                students { id }
                grantsGroup { id }
                licencedGroup { id }
                createdby { id }
                changedby { id }
                rbacobject { id }
            }
        }
    }"""
    },             
    "acprogramlanguages": {
        "read": """query($id: UUID!){ result: acProgramLanguageTypeById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acProgramLanguageTypePage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $name: String!, $name_en: String) {
        result: programLanguageTypeInsert(languageType: {id: $id, name: $name, nameEn: $name_en}) {
            id
            msg
            result: programLanguageType {
                id
                lastchange
                name
                nameEn
            }
        }
    }"""
    },             
    "acprogramlevels": {
        "read": """query($id: UUID!){ result: acProgramLevelTypeById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acProgramLevelTypePage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $name: String!, $name_en: String) {
        result: programLevelTypeInsert(levelType: {id: $id, name: $name, nameEn: $name_en}) {
            id
            msg
            result: programLevelType {
                id
                lastchange
                name
                nameEn
            }
        }
    }"""
    },
    "acprograms_studentmessages": {
        "read": """query($id: UUID!){ result: acProgramMessageById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acProgramMessagePage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation (
            $id: UUID!, $name: String!, $description: String
            $student_id: UUID!, $program_id: UUID!,
            $date: DateTime!
        ) {
        result: programMessageInsert(message: 
            {
                id: $id, name: $name, description: $description
                studentId: $student_id, programId: $program_id
                date: $date
            }) {
            id
            msg
            result: message {
                id
                name
                description
                date

                student { id }
                program { id }

            }
        }
    }"""
    },
    "acprograms_students": {
        "read": """query($id: UUID!){ result: acProgramStudentById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acProgramStudentPage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation (
            $id: UUID!, $student_id: UUID!, $program_id: UUID!,
                $state_id: UUID!, $semester: Int
        ) {
        result: programStudentInsert(student: {
                id: $id, studentId: $student_id, programId: $program_id,
                stateId: $state_id, semester: $semester
            }) {
            id
            msg
            result: student {
                id
                lastchange
                student { id }
                messages { id }
                state { id }
            }
        }
    }"""
    },                     
    "acprogramtitles": {
        "read": """query($id: UUID!){ result: acProgramTitleTypeById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acProgramTitleTypePage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $name: String!, $name_en: String) {
        result: programTitleTypeInsert(titleType: {id: $id, name: $name, nameEn: $name_en}) {
            id
            msg
            result: programTitleType {
                id
                lastchange
                name
                nameEn
            }
        }
    }"""
    },                     
    "acprogramtypes": {
        "read": """query($id: UUID!){ result: acProgramTypeById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acProgramTypePage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $name: String!, $name_en: String, 
        $title_id: UUID!, $form_id: UUID!, $language_id: UUID!, $level_id: UUID!) {
        result: programTypeInsert(programType: 
            {
                id: $id, name: $name, nameEn: $name_en
                titleId: $title_id, formId: $form_id, 
                languageId: $language_id, levelId: $level_id
            }) {
            id
            msg
            result: programType {
                id
                name
                nameEn
                level { id }
                form { id }
                language { id }
                title { id }
            }
        }
    }"""
    },                     
    "acsemesters": {
        "read": """query($id: UUID!){ result: acSemesterById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acSemesterPage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $subject_id: UUID!, $classificationtype_id: UUID!) {
        result: programSemesterInsert(semester: {
                id: $id, subjectId: $subject_id,
                classificationtypeId: $classificationtype_id
            }) {
            id
            msg
            result: semester {
                id
                lastchange
                order

                subject { id }
                classifications { id }
                classificationType { id }
                topics { id }

            }
        }
    }"""
    },                         
    "acprograms_studentstates": {
        "read": """query($id: UUID!){ result: acProgramStudentStateById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acProgramStudentStatePage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation (
            $id: UUID!, $name: String!, $name_en: String
            ) {
        result: programStudentStateInsert(studentState: 
            {
                id: $id, name: $name, nameEn: $name_en
            }) {
            id
            msg
            result: studentState {
                id
                name
                nameEn
            }
        }
    }"""
    },                         
    "acsubjects": {
        "read": """query($id: UUID!){ result: acSubjectById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acSubjectPage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $name: String!, $name_en: String, 
            $program_id: UUID!, $group_id: UUID!
        ) {
        result: programSubjectInsert(subject: {
            id: $id, name: $name, nameEn: $name_en
            programId: $program_id, groupId: $group_id
        }) {
            id
            msg
            result: subject {
                id
                lastchange
                name
                nameEn
                program { id }
                semesters { id }
                grants { id }
            }
        }
    }"""
    },                         
    "actopics": {
        "read": """query($id: UUID!){ result: acTopicById(id: $id) { id } }""",
        "readp": """query($skip: Int, $limit: Int){ result: acTopicPage(skip: $skip, limit: $limit) { id } }""",
        "create": """mutation ($id: UUID!, $semester_id: UUID!, $name: String!, $name_en: String) {
        result: programTopicInsert(topic: {
                id: $id, name: $name, nameEn: $name_en,
                semesterId: $semester_id
            }) {
            id
            msg
            result: topic {
                id
                lastchange
                name
                nameEn

                order
                semester { id }
                lessons { id }
            }
        }
    }"""
    }                     
}

# @pytest.mark.asyncio
# async def test_FillDataViaGQL(DemoFalse, FillDataViaGQL, ClientExecutorAdmin, DemoData):
# # async def test_FillDataViaGQL(DemoFalse, FillDataViaGQL, ClientExecutorAdmin, DemoData):
#     return
#     # for tableName, ops in queries.items():
#     #     table = DemoData.get(tableName, None)
#     #     assert table is not None, f"Missing {tableName} in DemoData source"
#     #     readQuery = ops.get("read", None)
#     #     assert readQuery is not None, f"missing read op on table {tableName}"
#     #     createQuery = ops.get("create", None)
#     #     assert createQuery is not None, f"missing create op on table {tableName}"

#     #     for row in table:
#     #         rowid = row.get("id", None)
#     #         assert rowid is not None, f"missing id key somewhere in table {tableName}"

#     #         variables = {**rowid}
#     #         resp = await ClientExecutorAdmin(query=readQuery, variable_values=variables)
#     #         result = resp["data"]["result"]
#     #         if result:
#     #             continue

#     #         # row does not exists
#     #         variables = {**rowid}
#     #         resp = await ClientExecutorAdmin(query=createQuery, variable_values=variables)


