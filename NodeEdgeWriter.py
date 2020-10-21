import csv

list_majors = ['American Studies', 'Anthropology', 'Applied Math', 'Art', 'Asian Studies', 'Biology', 'Chemistry',
          'Chinese', 'Classical', 'Computer Science', 'Economics', 'Educational Studies', 'English', 'Environmental Studies',
          'French', 'Geography', 'Geology', 'German', 'History', 'International Studies', 'Japanese', 'Latin American Studies',
          'Linguistics', 'Mathematics', 'Media and Cultural Studies', 'Music', 'Neuroscience', 'Philosophy', 'Physics',
          'Political Science', 'Psychology', 'Religious Studies', 'Russian', 'Sociology', 'Spanish', 'Theater and Dance',
          'Women\'s Gender and Sexuality Studies', 'Data Science', 'Statistics']

def fixMajors(student_majors):
    fixed_majors = []
    for major in list_majors:
        if major in student_majors:
            fixed_majors.append(major)
    if 'Theater' in student_majors or 'Theatre' in student_majors:
        fixed_majors.append('Theater and Dance')
    if 'International/Global Studies' in student_majors:
        fixed_majors.append('International Studies')
    if 'Communication' in student_majors:
        fixed_majors.append('Media and Cultural Studies')
    if 'Applied Math' in fixed_majors and 'Mathematics' in fixed_majors:
        fixed_majors.remove('Mathematics')
    if 'Art History' in student_majors:
        if student_majors.count('History') <= 1:
            fixed_majors.remove('History')
    return fixed_majors


def createMajorCompanyNetwork(reader):
    '''This function takes in the iterator over a CSV file and returns a dictionary with two dictionary entries.
    The first dictionary entry is the nodes dictionary and the second is the edges dictionary.
    The node dictionary includes the majors and companies of all students.
    The edge dictionary includes the source (major), target (company), and weight equivalent to the number of students
    with that major working for that company.
    This funtion also writes out the node and edge dictionaries as node and edge CSV files for Gephi.
    '''

    print("compiling nodes and edges")

    id=0
    nodes={}; edges={}

    for major in list_majors:
        nodes[major] = {'id': id, 'name': major, 'type_node': 'major'}
        id+=1

    row_count = 0
    student_companies = []

    for row in reader:
        name = row[0]
        school = row[1]
        majors = row[3]
        company = row[6]

        if name!="":
            if row_count > 0:
                for comp in student_companies:
                    target = nodes[comp]['id']
                    for maj in student_majors:
                        source = nodes[maj]['id']
                        edge_key = str([source, target])
                        if edge_key in edges:
                            edges[edge_key]['weight'] += 1
                        else:
                            edges[edge_key] = {
                                'source': source,
                                'target': target,
                                'weight': 1,
                                'major': maj
                            }

            student_companies = []
            student_majors = []

        if '\n' in company:
            split = company.split('\n')
            company = split[0]

        if 'Macalester' in company:
            company = "Macalester College"

        if company not in nodes:
            nodes[company] = {'id': id, 'name':company, 'type_node': 'company'}
            id+=1
        if company not in student_companies:
            student_companies.append(company)

        if school == 'Macalester College':
            student_majors = fixMajors(majors)

        row_count+=1

    print("writing node file")
    node_file = 'MajorCompanyNodes.csv'
    node_writer = csv.writer(open(node_file, 'w'))
    node_writer.writerow(['Id', 'Label', 'Type_Node'])

    for node_label, node_id in nodes.items():
        id = node_id['id']
        label = node_id['name']
        node_type = node_id['type_node']
        node_writer.writerow([id, label, node_type])

    print("writing edge file")
    edge_file = 'MajorCompanyEdges.csv'
    edge_writer = csv.writer(open(edge_file, 'w'))
    edge_writer.writerow(['Source', 'Target', 'Weight', 'Major'])

    for edge_value in edges.values():
        source = edge_value['source']
        target = edge_value['target']
        weight = edge_value['weight']
        major = edge_value['major']
        edge_writer.writerow([source, target, weight, major])

    return {'nodes': nodes, 'edges': edges}

if __name__ == "__main__":
    in_file = 'MacMerged.csv'

    reader = csv.reader(open(in_file, 'r'))
    next(reader)  # skip header

    createMajorCompanyNetwork(reader)


