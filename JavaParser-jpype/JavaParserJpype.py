import os
import jpype.imports

# JavaParser JAR 경로
JAVAPARSER_JAR = "javaparser-core-3.26.3.jar"

# JVM 시작
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[JAVAPARSER_JAR])

# JavaParser import
from com.github.javaparser import StaticJavaParser
from java.io import StringReader


def read_java_files(directory):
    """
    주어진 디렉토리에서 .java 파일을 찾아 내용 출력
    """
    java_files = find_java_files(directory)

    if not java_files:
        print("📌 .java 파일이 없습니다.")
        return

    print(f"📌 {len(java_files)}개의 .java 파일을 찾았습니다:\n")

    for java_file in java_files:
        with open(java_file, "r", encoding="utf-8") as f:
            java_code = f.read()
            java_parsing(java_code)

def find_java_files(directory):
    """
    주어진 디렉토리 내 모든 .java 파일을 찾아 리스트로 반환
    """
    java_files = []

    # os.walk()를 사용하여 하위 디렉토리까지 탐색
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):  # .java 파일만 필터링
                java_files.append(os.path.join(root, file))

    return java_files

def java_parsing(java_code):
    compilation_unit = StaticJavaParser.parse(StringReader(java_code))

    class_declarations = compilation_unit.findAll(
        jpype.JClass("com.github.javaparser.ast.body.ClassOrInterfaceDeclaration"))
    class_name = class_declarations[0].getNameAsString() if class_declarations else "클래스 없음"
    print(f"📌 클래스명: {class_name}")

    # 메서드 정보 추출
    methods = compilation_unit.findAll(jpype.JClass("com.github.javaparser.ast.body.MethodDeclaration"))

    print("\n📌 메서드 목록:")
    for method in methods:
        method_name = method.getNameAsString()  # 메서드 이름
        return_type = method.getType().toString()  # 반환 타입
        access_modifier = "default"  # 기본 접근 제어자 (패키지 레벨)

        # 접근 제어자 찾기
        modifiers = method.getModifiers()
        if modifiers.toString():
            access_modifier = " ".join([str(m) for m in modifiers])

        # 파라미터 추출
        parameters = method.getParameters()
        param_list = [f"{param.getType()}" for param in parameters]

        # 시그니처 출력
        print(f"  🔹 {return_type} {method_name}({', '.join(param_list)})")

        try :
            method_body = method.getBody().get().toString()  # 메서드 내용 (코드 블록)
            print(f"  🔹 내용:\n{method_body}\n")
        except Exception as e:
            pass



#read_java_files("최상위 디렉토리 입력")

# 예시
read_java_files("/home/simsim/IdeaProjects/deadLock/src")

